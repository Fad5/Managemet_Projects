# projects/admin.py

from django.contrib import admin
from .models import Project, ProjectStage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'created_date', 'start_date', 'completion_percentage')
    list_filter = ('created_date',)  # Убрали project_month
    search_fields = ('project_name', 'description')
    readonly_fields = ('created_date', 'created_at', 'project_month')  # Добавили project_month как readonly

    def project_month(self, obj):
        return obj.project_month  # Используем свойство из модели
    project_month.short_description = 'Месяц проекта'

@admin.register(ProjectStage)
class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'project', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'project', 'assigned_to')
    search_fields = ('stage_name',)