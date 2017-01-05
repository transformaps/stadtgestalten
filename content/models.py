from . import querysets
import core.models
from django.core import urlresolvers
from django.db import models
from django.utils import timezone


class Image(models.Model):
    content = models.ForeignKey('Content', blank=True, null=True, related_name='images')
    file = models.ImageField('Datei')
    weight = models.PositiveSmallIntegerField(default=0)
    creator = models.ForeignKey('gestalten.Gestalt', related_name='+', null=True, blank=True)

    class Meta:
        ordering = ('weight',)


class Base(core.models.Model):
    author = models.ForeignKey(
            'gestalten.Gestalt',
            related_name='authored_%(class)s')
    date_created = models.DateTimeField(default=timezone.now)
    text = models.TextField('Text')

    class Meta:
        abstract = True
        ordering = ('-date_created',)


class Comment(Base):
    content = models.ForeignKey('Content', related_name='comments')

    class Meta:
        ordering = ('date_created',)

    def get_content(self):
        return self.content


class Content(Base):
    subclass_names = ['Article', 'Event', 'Gallery']

    additional_authors = models.ManyToManyField(
            'gestalten.Gestalt', related_name='additional_authorship')
    comment_authors = models.ManyToManyField(
            'gestalten.Gestalt', through='Comment', related_name='comments')
    public = models.BooleanField(
            'Veröffentlichen',
            default=False,
            help_text='Veröffentlichte Beiträge sind auch für Besucherinnen '
            'sichtbar, die nicht Mitglied der Gruppe sind.'
            )
    slug = models.SlugField(default=None, null=True, unique=True)
    title = models.CharField('Titel', max_length=255)

    objects = models.Manager.from_queryset(querysets.ContentQuerySet)()

    def __str__(self):
        return self.title

    def add_to_additional_authors(self, gestalt):
        if not self.additional_authors.filter(id=gestalt.id):
            self.additional_authors.add(gestalt)

    def get_absolute_url(self):
        if not self.public:
            return urlresolvers.reverse('internal-content', args=[self.pk])
        try:
            return urlresolvers.reverse(
                    'content',
                    args=[self.groups.first().slug, self.slug]
                    )
        except AttributeError:
            return urlresolvers.reverse(
                    'gestalt-content',
                    args=[self.author.user.username, self.slug]
                    )

    def get_content(self):
        return self.get_subclass_instance()

    def get_display_type_name(self):
        return self.get_subclass_instance().get_display_type_name()

    def get_subclass_instance(self):
        import sys
        for subclass_name in self.subclass_names:
            try:
                return getattr(self, subclass_name.lower())
            except getattr(sys.modules[__name__], subclass_name).DoesNotExist:
                pass

    def get_type_name(self):
        return self.get_subclass_instance()._meta.model_name


class Article(Content):
    objects = models.Manager.from_queryset(querysets.ContentQuerySet)()

    def get_display_type_name(self):
        return 'Artikel' if self.public else 'Interner Artikel'


class Event(Content):
    place = models.CharField('Ort / Anschrift', max_length=255)
    time = models.DateTimeField('Datum / Uhrzeit')
    all_day = models.BooleanField('ganztägig', default=False)
    until_time = models.DateTimeField('Datum / Uhrzeit Ende', blank=True, null=True)

    objects = models.Manager.from_queryset(querysets.EventQuerySet)()

    class Meta:
        ordering = ('time',)

    def date(self):
        return self.time.date()

    def get_display_type_name(self):
        return 'Ereignis' if self.public else 'Internes Ereignis'


class Gallery(Content):
    objects = models.Manager.from_queryset(querysets.ContentQuerySet)()

    def get_display_type_name(self):
        return 'Galerie' if self.public else 'Interne Galerie'
