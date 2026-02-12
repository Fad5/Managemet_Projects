# projects/templatetags/project_filters.py

from django import template

register = template.Library()

@register.filter
def length_by_completion(projects, target_percentage):
    """Фильтр для подсчета проектов по проценту выполнения"""
    if target_percentage == 0:
        return sum(1 for p in projects if p.completion_percentage == 0)
    elif target_percentage == 100:
        return sum(1 for p in projects if p.completion_percentage == 100)
    else:
        return sum(1 for p in projects if 0 < p.completion_percentage < 100)