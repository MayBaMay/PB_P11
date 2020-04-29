from django.urls import path
from django.contrib.auth import views as auth_views

from . import views # import views so we can use them in urls.

app_name = 'foodSearch'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('search/', views.search, name='search'),
    path('results/<int:product_id>/', views.results, name='results'),
    path('detail/<int:product_id>/', views.detail, name='detail'),
    path('userpage/', views.userpage, name='userpage'),
    path('new_name/', views.new_name, name='new_name'),
    path('new_email/', views.new_email, name='new_email'),
    path('load_favorite/', views.load_favorite, name='load_favorite'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('legals/', views.legals, name='legals'),

    # Password reset
    #(ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
             ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
             ),
         name='password_reset_done'),

    path('reset/{uidb64}/{token}/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
             ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
             ),
         name='password_reset_complete'),
]
