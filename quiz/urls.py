from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('quiz/<int:id>/', views.quiz, name='quiz'),
    path(
        'quiz/<int:id>/subcategory/<int:subcategory_id>/',
        views.subcategory_quiz,
        name='subcategory_quiz'
    ),

    path('my-results/', views.my_results, name='my_results'),

    path('leaderboard/', views.leaderboard, name='leaderboard'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
