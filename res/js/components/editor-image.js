import { $, getAttr, remove, toggleClass } from 'luett'
import { sum } from 'lodash'
import bel from 'bel'
import EventEmitter from 'eventemitter3'

import { image as adapter } from '../adapters/api'
import pickii from './pickii'
import filePicker from './file-picker'
import tabbed from './tabbed'
import progress from './progress'

const contentId = getAttr($("[name='content_id']"), 'value', false)

let processIds = 0

function progressAdapterFactory(callback) {
  const iface = {}
  const handlers = []

  function propagateProgress() {
    const progress = sum(handlers) / handlers.length
    callback({
      complete: Math.max(0, Math.min(100, progress)),
      jobCount: handlers.length
    })
  }

  iface.createHandler = () => {
    const id = handlers.length
    handlers[id] = 0
    return progress => {
      if(progress.lengthComputable) {
        handlers[id] = progress.loaded / progress.total * 100
        propagateProgress()
      }
    }
  }

  return iface
}

function upload (files, onProgress) {
  const progressAdapter = progressAdapterFactory(onProgress)
  const uploads = files.map(file => {
    return adapter.create({file, contentId}, {onProgress: progressAdapter.createHandler()})
  })
  return Promise.all(uploads)
}

function dummyAdapter () {
  return Promise.resolve([])
}

function createFilePicker (emitter) {
  return filePicker({
    accept: ['image/png', 'image/gif', 'image/jpeg', 'capture=camera'],
    multiple: true,
    callback: (files) => {
      const processId = processIds++
      emitter.emit('files:upload', { files, processId })
      upload(files, progress => emitter.emit('files:progress', { progress, processId }))
        .then((files) => {
          emitter.emit('files:select', files)
          emitter.emit('files:add', files)
          emitter.emit('files:done', { files, processId })
        })
    },
    trigger: bel`<button type="button" class="btn btn-link btn-sm">
    <i class="sg sg-add"></i> Hinzufügen
</button>`
  })
}

function createContentImageView (emitter) {
  return pickii({
    emit: emitter.emit.bind(emitter),
    adapter: contentId ? () => adapter.get({content: contentId}) : dummyAdapter
  })
}

function createUserImageView (emitter) {
  const creator = window.app.conf.gestalt.id
  return pickii({
    emit: emitter.emit.bind(emitter),
    adapter: creator ? () => adapter.get({creator}) : dummyAdapter
  })
}

function createTabbed (emitter, tabConfig = {}) {
  const opts = Object.assign({}, {user: true, content: true}, tabConfig)
  const tabs = []

  if (opts.content) {
    const contentImageView = createContentImageView(emitter)
    emitter.on('files:add', contentImageView.refresh)
    tabs.push({
      content: contentImageView.el,
      label: bel`<span>Beitragsbilder</span>`
    })
  }

  if (opts.user) {
    const userImageView = createUserImageView(emitter)
    emitter.on('files:add', userImageView.refresh)
    tabs.push({
      content: userImageView.el,
      label: bel`<span>Deine Bilder</span>`
    })
  }

  return tabbed({tabs})
}

export default (opts = {}) => {
  const iface = {}
  const emitter = new EventEmitter()
  let progressBar

  const imageEditor = bel`<div class="editor-images">
    <div class="btn-toolbar btn-toolbar-spread">
        <h3>Bilder</h3>
        ${createFilePicker(emitter).el}
    </div>
    ${createTabbed(emitter, opts.tabs).el}
</div>`

  iface.remove = function () {
    remove(imageEditor)
    if (progressBar) {
      progressBar.destroy()
    }
  }

  iface.emitter = emitter
  iface.el = imageEditor

  emitter.on('files:upload', event => {
    toggleClass(imageEditor, 'editor-images-upload', true)
    progressBar = progress({
      description: `${event.files.length} ${event.files.length == 1 ? 'Bild wird' : 'Bilder werden'} hochgeladen`
    })
    imageEditor.appendChild(progressBar.el)
  })

  emitter.on('files:progress', event => {
    progressBar.setProgress(event.progress.complete)
  })

  emitter.on('files:done', () => {
    progressBar.remove()
    remove(progressBar.el)
    toggleClass(imageEditor, 'editor-images-upload', false)
  })

  return iface
}
