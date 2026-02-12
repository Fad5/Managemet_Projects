from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from projects import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.project_list, name='project_list'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path('projects/', include('projects.urls')),  # Все URL проектов
]

# Тестовые URL для 404 и 500 (ДОБАВЛЯЕМ В urlpatterns, а не отдельно)
urlpatterns += [
    path('test-404/', TemplateView.as_view(template_name='errors/404.html')),
    path('test-500/', TemplateView.as_view(template_name='errors/500.html')),
    path('test-400/', TemplateView.as_view(template_name='errors/400.html')),
]

# Обработчики ошибок
handler404 = 'projects.views.handler404'
handler500 = 'projects.views.handler500'
handler400 = 'projects.views.handler400'