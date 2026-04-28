from django.contrib.auth import views as auth_views
from django.urls import path

from users import views

urlpatterns = [
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("", views.user_list, name="user_list"),
    path("create/", views.user_create, name="user_create"),
    path("<int:user_id>/edit/", views.user_edit, name="user_edit"),
    path("roles/", views.role_list, name="role_list"),
    path("roles/create/", views.role_create, name="role_create"),
    path("roles/<int:role_id>/edit/", views.role_edit, name="role_edit"),
    path("roles/<int:role_id>/delete/", views.role_delete, name="role_delete"),
    path("roles/assign/", views.role_assign, name="role_assign"),
]
