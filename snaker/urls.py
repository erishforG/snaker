from django.conf.urls import include, url
from shortner.views import shortner_view, tag_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [

    #admin
    url(r'^admin/', include('session.urls')),

    #shortner
    url(r'^urls/', include('shortner.urls')),

    url(r'^url/detail/$', shortner_view.url_detail, name="url_detail"),

    url(r'^url/(?P<hash>\w+)/$', shortner_view.url_data_controller, name='url_data_controller'),

    # tag
    url(r'^tag/$', tag_view.tag_list_controller, name='tag_list_controller'),

    #hash
    url(r'^(?P<hash>\w+)/$', shortner_view.url_change_controller, name='url_change_controller'),

    url(r'^(?P<hash>\w+)/iframe/$', shortner_view.url_iframe_controller, name='url_iframe_controller'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, insecure=True) + staticfiles_urlpatterns()
