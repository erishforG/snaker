from django.conf.urls import url

from session.views import session_views

urlpatterns = [

    # tracker
    url(r'^login/$', session_views.login_controller, name='login_controller'),

    url(r'^logout/$', session_views.logout_controller, name='logout_controller'),

]