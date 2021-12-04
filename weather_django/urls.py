from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 添加app路由
    path('', include('proj.urls')),
]
