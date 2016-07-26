from . import views
from django.conf import urls

urlpatterns = [
    urls.url(
        r'^groups/(?P<group_pk>[0-9]+)/join/$',
        views.Join.as_view(),
        name='join'),

    urls.url(
        r'^groups/(?P<group_pk>[0-9]+)/members/$',
        views.Members.as_view(),
        name='members'),

    urls.url(
        r'^groups/(?P<group_pk>[0-9]+)/members/add$',
        views.MemberCreate.as_view(),
        name='member-create'),

    urls.url(
        r'^groups/(?P<group_pk>[0-9]+)/resign/$',
        views.Resign.as_view(),
        name='resign'),
]