from django.contrib import admin
from django.urls import path, re_path
from firstApp import views
from django.conf.urls.static import static
from django.conf import settings
from firstApp.views import view_pose_description
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$', views.index, name='homepage'),
    re_path('predictImage', views.predictImage, name='predictImage'),
    re_path('viewDataBase', views.viewDataBase, name='viewDataBase'),
    re_path('view_pose_description/', view_pose_description, name='view_pose_description'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
