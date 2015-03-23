from django.conf.urls import patterns, include, url
from django.contrib import admin
from childquestions import views
 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChildLearning.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', views.homepage),
    url(r'^problem/', views.problems),
    url(r'^result/', views.problemSubmit),
    url(r'^problemSelect/', views.problemSelect),
    url(r'^sendProblem/', views.problemSend),
     url(r'^rewards/', views.rewards),
    url(r'^respgroup/(?P<respgroup>\w+)/$', views.all_json_answers),
    )
