# projects/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Project, ProjectStage, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__role')
    
    def get_role(self, obj):
        return obj.profile.role
    get_role.short_description = 'Роль'

# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'role', 
        'can_create_projects', 'can_edit_projects', 'can_delete_projects',
        'can_create_stages', 'can_edit_stages', 'can_delete_stages',
        'can_manage_users'
    )
    list_filter = (
        'role', 
        'can_create_projects', 'can_edit_projects', 'can_delete_projects',
        'can_create_stages', 'can_edit_stages', 'can_delete_stages'
    )
    search_fields = ('user__username',)
    
    fieldsets = (
        ('Основное', {
            'fields': ('user', 'role')
        }),
        ('Права на проекты', {
            'fields': ('can_create_projects', 'can_edit_projects', 'can_delete_projects')
        }),
        ('Права на этапы', {
            'fields': ('can_create_stages', 'can_edit_stages', 'can_delete_stages')
        }),
        ('Администрирование', {
            'fields': ('can_manage_users',)
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'created_date', 'completion_percentage', 'created_by')
    list_filter = ('created_date',)
    search_fields = ('project_name', 'description')
    readonly_fields = ('created_date', 'created_at', 'project_month')

@admin.register(ProjectStage)
class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'project', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'project', 'assigned_to')
    search_fields = ('stage_name',)