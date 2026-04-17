from django.urls import path

from apps.dashboard.views import DashboardHomeView, ExportView, StatisticsView, UserManagementView


app_name = "dashboard"

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="home"),
    path("statistics/", StatisticsView.as_view(), name="statistics"),
    path("users/", UserManagementView.as_view(), name="users"),
    path("export/", ExportView.as_view(), name="export"),
]
