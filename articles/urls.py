from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<slug:slug>", views.detail, name="detail"),
    path("create/article", views.create_article, name="create-article"),
    path("update/article/<slug:slug>", views.update_article, name="update-article"),
    path("delete/article/<slug:slug>", views.delete_article, name="delete-article"),
    path("apply/<slug:slug>", views.apply_request, name="apply-request"),
    path("manage/requests", views.manage_requests, name="manage-requests"),
    path("update/request/<int:request_id>", views.update_request_status, name="update-request-status"),
    path("student-applications/", views.student_applications, name="student-applications"),

    path("user/profile/<int:user_id>/", views.view_user_profile, name="view-user-profile"),
]
