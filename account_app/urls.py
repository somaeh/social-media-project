from django.urls import path
from .import views

app_name = "account_app"
urlpatterns =[
     path('register', views.RegisterView.as_view(), name="register"),
     path('login', views.UserLoginView.as_view(), name="login"),
     path('logout', views.UserLogoutView.as_view(), name="logout"),
     path('profile/<int:user_id>/', views.UserProfileView.as_view(), name="profile"),
     path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='follow'),
     path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name='unfollow'),
     path('edit_user/', views.EditUserView.as_view(), name="edit_user"),
     
]