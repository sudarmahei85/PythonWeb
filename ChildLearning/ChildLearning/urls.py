from django.conf.urls import patterns, include, url
from django.contrib import admin
from childquestions import views
 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChildLearning.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    
    url(r'^problem/', views.problems),
    url(r'^result/', views.problemSubmit),
    url(r'^sendProblem/', views.problemSend),
    )
