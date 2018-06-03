from django.conf.urls import include, url
from shortner.views import shortener_view, tag_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [

    #admin
    url(r'^login/$', auth_views.login, name='login'),

    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^admin/', admin.site.urls),

    #shortner
    url(r'^urls/', include('shortner.urls')),

    url(r'^url/detail/$', shortener_view.url_list_tag_controller, name="url_detail"),

    # tag
    url(r'^tag/$', tag_view.tag_list_controller, name='tag_list_controller'),

    #hash
    url(r'^(?P<hash>\w+)/$', shortener_view.url_change_controller, name='url_change_controller'),

    url(r'^(?P<hash>\w+)/iframe/$', shortener_view.url_iframe_controller, name='url_iframe_controller'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, insecure=True) + staticfiles_urlpatterns()
