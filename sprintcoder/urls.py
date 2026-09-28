from django.contrib import admin
from django.urls import path, include
from trainer import analytics

urlpatterns = [
    path('admin/analytics/', analytics.admin_analytics_view, name='admin_analytics'),
    path('admin/analytics/api/', analytics.admin_analytics_api, name='admin_analytics_api'),
    path('admin/analytics/export/<str:export_type>/', analytics.admin_export_csv, name='admin_export_csv'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('trainer.urls')),
]

