from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvaluationViewSet, get_applied_user_list, get_document_pass_count, get_user_evaluation, set_document_pass, unset_document_pass, set_final_pass, unset_final_pass, get_user_applications, get_admin_evaluation_status, update_evaluation

router = DefaultRouter()
router.register(r"evaluations", EvaluationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "get-applied-user-list/", get_applied_user_list, name="get-applied-user-list"
    ),  # 1번
    path(
        "document-pass-count/<int:post_id>/",
        get_document_pass_count,
        name="first-round-pass-count",
    ),  # 2번
    path(
        "user-evaluation/<int:user_id>/", get_user_evaluation, name="user-evaluation"
    ),  # 3번
    path("set-document-pass/", set_document_pass, name="set_document_pass"),  # 5-1번
    path(
        "unset-document-pass/", unset_document_pass, name="unset_document_pass"
    ),  # 5-2번
    path("set-final-pass", set_final_pass, name="set_final_pass"),  # 6-1번
    path("unset-final-pass/", unset_final_pass, name="unset_final_pass"),  # 6-2번
    path(
        "get-user-applications/<int:apply_id>/",
        get_user_applications,
        name="application-details",
    ),  # 7번
    path(
        "admin-evaluation-status/<int:user_id>/",
        get_admin_evaluation_status,
        name="admin-evaluation-status",
    ),  # 8번
    path(
        "update-evaluation/<int:evaluation_id>/",
        update_evaluation,
        name="update-evaluation",
    ),  # 9번
]
