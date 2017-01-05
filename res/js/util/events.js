import EventEmitter from 'eventemitter3'

function evented (obj) {
  Object.assign(obj, EventEmitter.prototype)
  return obj
}

function eventedFunction (func) {
  function wrapper () {
    wrapper.emit('dispatch', arguments)
    const result = func.apply(this, arguments)
    wrapper.emit('call', result)
    return result
  }
  evented(wrapper)
  return wrapper
}

export { evented, eventedFunction }
