from django import forms
from entities import models as entities_models
import functools


class Field:
    def __init__(self, view):
        self.view = view

    def clean(self, form):
        pass

    def get_form_field(self):
        return None

    def get_layout(self):
        return None

    def get_model_form_field(self):
        return None

    def get_name(self):
        return self.name


def fieldclass_factory(superclass, name):
    classname = name.replace('_', '').capitalize() + superclass.__name__
    return type(classname, (superclass,), {'name': name})


class CurrentGestalt(Field):
    def clean(self, form):
        if not self.view.request.user.is_authenticated():
            try:
                gestalt = entities_models.Gestalt.objects.get(
                        user__email=form.cleaned_data.get(self.get_name()))
                if gestalt.can_login():
                    form.add_error(self.get_name(), forms.ValidationError(
                        'Es gibt bereits ein Benutzerkonto mit dieser '
                        'E-Mail-Adresse. Bitte melde Dich mit E-Mail-Adresse '
                        'und Kennwort an.', code='existing'))
            except entities_models.Gestalt.DoesNotExist:
                pass

    def get_data(self, form_data):
        if self.view.request.user.is_authenticated():
            return self.view.request.user.gestalt
        else:
            return entities_models.Gestalt.create_unusable(form_data)

    def get_form_field(self):
        return self.if_not_authenticated(
                forms.EmailField(label='E-Mail-Adresse'))

    def get_layout(self):
        return self.if_not_authenticated(self.get_name())

    def get_name(self):
        return self.if_not_authenticated('{}_email'.format(self.name))

    def if_not_authenticated(self, v1, v2=None):
        return v1 if not self.view.request.user.is_authenticated() else v2

current_gestalt = functools.partial(fieldclass_factory, CurrentGestalt)


class RelatedObject(Field):
    def get_data(self, form_data):
        return self.view.related_object

related_object = functools.partial(fieldclass_factory, RelatedObject)
