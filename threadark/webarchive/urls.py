from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .classes.ThreadStorage import ThreadStorage
from .classes.ArchiveExplorer import ArchiveExplorer

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', views.custom_logout, name='logout'),

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<str:board>/view-catalog/', views.view_catalog, name='view_catalog_with_board'),
    path('<str:board>/live-thread/<int:thread_id>/', views.view_live_thread, name='view_live_thread'),
    path('store/<str:board>/<int:thread_id>/', views.store_posts, name='store_posts'),
    path('<str:board>/thread/<int:thread_id>/', views.view_thread, name='view_thread'),
    path('<str:board>/list/', views.view_archive, name='view_archive_with_board'),
    path('<str:board>/data/', views.archive_data, name='get_archive_data'),
    path('<str:board>/audio/<int:thread_id>/', views.tts_audio, name='tts_audio'),
]