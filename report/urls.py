from django.urls import path

from . import views

app_name = 'report'
urlpatterns = [
    path('<int:instruction_id>/<str:url>', views.sar_request_code, name='request-code'),
    path('access-code/', views.sar_access_code, name='access-code'),
    path('access-code/<str:messages>', views.sar_access_code, name='access-code'),
    path('select-report/<str:token>', views.get_report, name='select-report')
]
