from django.conf.urls import patterns, include, url
from django.contrib import admin
from childquestions import views
from django.conf.urls.static import static
from django.conf import settings
 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChildLearning.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.loginpage),
     url(r'^logout/', views.logoutpage),
    url(r'^register/',views.register),
    url(r'^$', views.homepage),
    url(r'^problem/', views.problems),
    url(r'^result/', views.problemSubmit),
    url(r'^problemSelect/', views.problemSelect),
    url(r'^sendProblem/', views.problemSend),
     url(r'^rewards/', views.rewards),
    url(r'^respgroup/(?P<respgroup>\w+)/$', views.all_json_answers),
    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
