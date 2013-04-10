from django.conf.urls.defaults import *

urlpatterns = patterns('affiliates.views',
    (r'^report/(\w+)/$', 'affiliate_report'),
)
