from django.urls import path

from apps.dashboard.views import DashboardHomeView, ExportAllView, ExportDatasetView, ExportView, StatisticsView, UserManagementView


app_name = "dashboard"

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="home"),
    path("statistics/", StatisticsView.as_view(), name="statistics"),
    path("users/", UserManagementView.as_view(), name="users"),
    path("export/", ExportView.as_view(), name="export"),
    path("export/all/", ExportAllView.as_view(), name="export_all"),
    path("export/<str:dataset>/", ExportDatasetView.as_view(), name="export_dataset"),
]
