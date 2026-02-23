# projects/decorators.py

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

# Права для проектов
def can_create_project(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.can_create_projects or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        messages.error(request, 'У вас нет прав для создания проектов')
        return redirect('project_list')
    return _wrapped_view

def can_edit_project(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.can_edit_projects or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        messages.error(request, 'У вас нет прав для редактирования проектов')
        return redirect('project_list')
    return _wrapped_view

def can_delete_project(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.can_delete_projects or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        messages.error(request, 'У вас нет прав для удаления проектов')
        return redirect('project_list')
    return _wrapped_view

# Права для этапов
def can_create_stage(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.can_create_stages or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        messages.error(request, 'У вас нет прав для создания этапов')
        return redirect('project_list')
    return _wrapped_view

def can_edit_stage(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.can_edit_stages or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        messages.error(request, 'У вас нет прав для редактирования этапов')
        return redirect('project_list')
    return _wrapped_view

def can_delete_stage(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.can_delete_stages or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        messages.error(request, 'У вас нет прав для удаления этапов')
        return redirect('project_list')
    return _wrapped_view

def can_manage_users(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.can_manage_users or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        messages.error(request, 'У вас нет прав для управления пользователями')
        return redirect('project_list')
    return _wrapped_view