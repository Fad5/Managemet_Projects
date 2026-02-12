# projects/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User  
from .models import Project, ProjectStage
from .forms import CustomLoginForm, CustomUserCreationForm, ProjectForm, ProjectStageForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('project_list')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('project_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('login')

from django.db.models import Q

@login_required
def project_list(request):
    # Получаем уникальные месяцы для фильтрации из created_date
    months_raw = Project.objects.dates('created_date', 'month', order='DESC')
    months = [date.strftime('%Y-%m') for date in months_raw]
    
    # Параметры фильтрации
    selected_month = request.GET.get('month')
    completion_filter = request.GET.get('completion')
    search_query = request.GET.get('search', '').strip()
    
    # Начальный запрос
    projects = Project.objects.all().order_by('-created_date')
    
    # Поиск без учета регистра
    if search_query:
        projects = projects.filter(
            Q(project_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Фильтр по месяцу (из created_date)
    if selected_month:
        try:
            # Преобразуем YYYY-MM в дату
            year, month = map(int, selected_month.split('-'))
            # Фильтруем по году и месяцу
            projects = [
                p for p in projects 
                if p.created_date.year == year and p.created_date.month == month
            ]
        except:
            pass  # Если неправильный формат месяца
    
    # Фильтр по проценту выполнения
    if completion_filter:
        if completion_filter == '0':
            projects = [p for p in projects if p.completion_percentage == 0]
        elif completion_filter == '1-49':
            projects = [p for p in projects if 1 <= p.completion_percentage < 50]
        elif completion_filter == '50-99':
            projects = [p for p in projects if 50 <= p.completion_percentage < 100]
        elif completion_filter == '100':
            projects = [p for p in projects if p.completion_percentage == 100]
    
    # Статистика
    all_projects = Project.objects.all()
    total_projects = all_projects.count()
    
    # Счетчики для статистики
    not_started = sum(1 for p in all_projects if p.completion_percentage == 0)
    in_progress = sum(1 for p in all_projects if 0 < p.completion_percentage < 100)
    completed = sum(1 for p in all_projects if p.completion_percentage == 100)
    
    context = {
        'projects': projects,
        'months': months,
        'selected_month': selected_month,
        'search_query': search_query,
        'completion_filter': completion_filter,
        'total_projects': total_projects,
        'not_started': not_started,
        'in_progress': in_progress,
        'completed': completed,
    }
    
    return render(request, 'projects/project_list.html', context)

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    stages = project.stages.all()
    users = User.objects.filter(is_active=True)  # Добавьте эту строку
    
    if request.method == 'POST':
        if 'add_stage' in request.POST:
            stage_name = request.POST.get('stage_name')
            status = request.POST.get('status')
            assigned_to_id = request.POST.get('assigned_to')
            
            stage = ProjectStage(
                project=project,
                stage_name=stage_name,
                status=status
            )
            
            if assigned_to_id:
                try:
                    assigned_to = User.objects.get(id=assigned_to_id)
                    stage.assigned_to = assigned_to
                except User.DoesNotExist:
                    pass
            
            stage.save()
            messages.success(request, 'Этап успешно добавлен')
            return redirect('project_detail', pk=pk)
    
    context = {
        'project': project,
        'stages': stages,
        'users': users,  # Добавьте эту строку
        'completion_percentage': project.completion_percentage,
    }
    return render(request, 'projects/project_detail.html', context)

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект успешно создан')
            return redirect('project_list')
    else:
        form = ProjectForm()
    
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект успешно обновлен')
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/project_form.html', {'form': form, 'project': project})

@login_required
def stage_edit(request, pk):
    stage = get_object_or_404(ProjectStage, pk=pk)
    
    if request.method == 'POST':
        stage_name = request.POST.get('stage_name')
        status = request.POST.get('status')
        assigned_to_id = request.POST.get('assigned_to')
        
        # Обновляем данные этапа
        stage.stage_name = stage_name
        stage.status = status
        
        if assigned_to_id:
            try:
                assigned_to = User.objects.get(id=assigned_to_id)
                stage.assigned_to = assigned_to
            except User.DoesNotExist:
                stage.assigned_to = None
        else:
            stage.assigned_to = None
            
        stage.save()
        messages.success(request, 'Этап успешно обновлен')
        return redirect('project_detail', pk=stage.project.pk)
    
    # Получаем всех активных пользователей для выпадающего списка
    users = User.objects.filter(is_active=True)
    
    context = {
        'stage': stage,
        'users': users,
    }
    return render(request, 'projects/stage_edit.html', context)

@login_required
def stage_delete(request, pk):
    stage = get_object_or_404(ProjectStage, pk=pk)
    project_pk = stage.project.pk
    stage.delete()
    messages.success(request, 'Этап успешно удален')
    return redirect('project_detail', pk=project_pk)

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект успешно удален')
        return redirect('project_list')
    
    # Если GET запрос, перенаправляем на детали проекта
    return redirect('project_detail', pk=pk)

def handler404(request, exception):
    """Ошибка 404 - страница не найдена"""
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Ошибка 500 - внутренняя ошибка сервера"""
    return render(request, 'errors/500.html', status=500)

def handler400(request, exception):
    """Ошибка 400 - неверный запрос"""
    return render(request, 'errors/400.html', status=400)

def handler403(request, exception):
    """Ошибка 403 - доступ запрещен"""
    return render(request, 'errors/403.html', status=403)  # если понадобится