from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'testform.views.login', name='login'),
    url(r'^approve/fail/$', 'testform.views.request_result',{"result":"SUCCESS"}, name='approve_fail'),
    url(r'^approve/success/$', 'testform.views.request_result',{"result":"SUCCESS"}, name='approve_success'),
    url(r'^approve/', 'testform.views.approve_phone', name='approve'),
    url(r'^register/success/$', 'testform.views.request_result',{"result":"SUCCESS"}, name='registration_success'),
    url(r'^register/', 'testform.views.register', name='register'),
    

    #url(r'^admin/', include(admin.site.urls)),
)
