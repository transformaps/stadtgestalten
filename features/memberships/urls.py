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
        r'^groups/(?P<group_pk>[0-9]+)/members/add/$',
        views.MemberAdd.as_view(),
        name='member-create'),

    urls.url(
        r'^groups/(?P<group_pk>[0-9]+)/resign/$',
        views.Resign.as_view(),
        name='resign'),

    urls.url(
        r'^associations/(?P<association_pk>[0-9]+)/apply/$',
        views.Apply.as_view(),
        name='create-membership-application'),

    urls.url(
        r'^memberships/applications/(?P<application_pk>[0-9]+)/accept/$',
        views.AcceptApplication.as_view(),
        name='accept-membership-application'),
]
