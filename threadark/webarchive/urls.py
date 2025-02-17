from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('two-factor/', views.two_factor_view, name='two_factor'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
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