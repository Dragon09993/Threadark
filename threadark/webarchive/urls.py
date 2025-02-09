from django.urls import path
from . import views
from .classes.ThreadStorage import ThreadStorage
from .classes.ArchiveExplorer import ArchiveExplorer

urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<str:board>/view-catalog/', views.view_catalog, name='view_catalog_with_board'),
    path( '<str:board>/live-thread/<int:thread_id>/', views.view_live_thread, name='view_live_thread' ),
    path('store/<str:board>/<int:thread_id>/', views.store_posts, name='store_posts'),
    path( '<str:board>/thread/<int:thread_id>/', views.view_thread, name='view_thread' ),
    path( '<str:board>/list/', views.view_archive, name='view_archive_with_board' ),
    path( '<str:board>/list/<int:page>/', views.view_archive, name='view_archive_with_board' ),
]