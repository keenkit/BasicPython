from django.conf.urls import url, include
from Services import views

urlpatterns = [
    #url(r'^comments/$', views.comment_list),
    url(r'^announcement/$', views.announcement_detail),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.comment_detail),
    url(r'^evaluation/(?P<pk>[0-9]+)/$', views.evaluation_detail),
    url(r'^clearCaches/$', views.clear_caches),
    url(r'^clearCache/$', views.clear_cache),
]

# Login and logout views for the browsable API

# urlpatterns += [
#     url(r'^api-auth/', include('rest_framework.urls',
#                                namespace='rest_framework')),
# ]