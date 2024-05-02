from unicodedata import name
from django.urls import path
from authors import views

urlpatterns = [
    path('create-new-account/', views.signUp.as_view(), name="register"),
    path('user-profile/<str:user_name>/', views.profile.as_view(), name="profile"),
    # path('user-profile/<str:user_name>/', views.profile, name="profile"),
    path('login/', views.logIn.as_view(), name="login"),
    path('logout/', views.logOut.as_view(), name="logout"),
    path('change_password/', views.PasswordchangeView.as_view(template_name = "authors/password_change.html"), name="change-password"),
    path('password_success/', views.password_success, name="password_success"),
    path('edit_profile/', views.UpdateUserView.as_view(), name="edit_user"),
    path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name="delete_user"),
    path('update_public_details/', views.UpdatePublicDetails.as_view(), name="user_public_details"),
    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
    path('create-biography/', views.UserBiographyView.as_view(), name="create-biography"),
    path('update-biography/<int:pk>/', views.UpdateBiographyView.as_view(), name="update-biography"),
    path('biography/', views.ShowBiographyView.as_view(), name="biography"),

]
