from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path("register/", views.register_user, name="register"),
    # path("record/<int:pk>", views.customer_record, name="record"),
    # path("delete_record/<int:pk>", views.delete_record, name="delete_record"),
    # path("add_record/", views.add_record, name="add_record"),
    # path("update_record/<int:pk>", views.update_record, name="update_record"),
    # viewing for displaying
    path("", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("dashboard/<str:username>", views.dashboard, name="dashboard"),
    path("button/<str:username>", views.button_view, name="button"),
    path("typography/<str:username>", views.typography_view, name="typography"),
    path("element/<str:username>", views.typography_view, name="element"),
    path("widget/<str:username>", views.widget_view, name="widget"),
    path("form/<str:username>", views.form_view, name="form"),
    path("table/<str:username>", views.table_view, name="table"),
    path("chart/<str:username>", views.chart_view, name="chart"),
    path("signin/<str:username>", views.signin_view, name="signin"),
    path("signup/<str:username>", views.signup_view, name="signup"),
    path("404/<str:username>", views.view_404, name="404"),
    path("blank/<str:username>", views.blank_view, name="blank"),
    # path("add_cus_record/<str:username>", views.add_cus_record, name="add_cus_record"),
    # path("client_record/<int:pk>",views.client_record,name="client_record"),
    path("add_client_to_db/", views.add_client_to_db, name="add_client_to_db"),
    path(
        "add_client_view/<str:username>", views.add_client_view, name="add_client_view"
    ),
    path(
        "view_all_client/<str:username>", views.view_all_client, name="view_all_client"
    ),
    path("update_the_client/<int:pk>", views.update_client, name="update_client"),
    path("delete_the_client/<int:pk>", views.delete_client, name="delete_client"),
    # CREATE CASES TYPE
    path("case_type/<str:username>", views.case_type, name="case_type"),
    path("add_case_type/", views.add_case_type, name="add_case_type"),
    path("delete_case_type/<int:pk>/", views.delete_case_type, name="delete_case_type"),
    path("update_case_type/<int:pk>/", views.update_case_type, name="update_case_type"),
    # CREATE COURT TYPE
    path("court_type/<str:username>", views.court_type, name="court_type"),
    path("add_court_type/", views.add_court_type, name="add_court_type"),
    path(
        "delete_court_type/<int:pk>/", views.delete_court_type, name="delete_court_type"
    ),
    path(
        "update_court_type/<int:pk>/", views.update_court_type, name="update_court_type"
    ),
    # CASES
    path("list_case/<str:username>", views.list_case, name="list_case"),
    path("create_case_view/<str:username>/", views.create_case_view, name="create_case_view"),
    path("create_case_detail/", views.create_case_detail, name="create_case_detail"),
    path("update_case/<int:pk>/", views.update_case_client, name="update_case_client"),
    path("delete_case_client/<int:pk>/", views.delete_case, name="delete_case_client"),
    path("single_case_client/<int:pk>/", views.single_case_client, name="single_case_client"),
    # path(
    #     "add_client_to_case/<int:pk>",
    #     views.add_client_to_case,
    #     name="add_client_to_case",
    # ),
    # path(
    #     "add_case_clients/<str:username>/",
    #     views.add_case_clients,
    #     name="add_case_clients",
    # ),
]
