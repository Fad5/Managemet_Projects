# projects/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, IntegerField

# projects/models.py

class Project(models.Model):
    project_name = models.CharField(max_length=100, unique=True, verbose_name="Название проекта")
    # Убираем project_month - будет вычисляться из created_date
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)  # Автоматически
    start_date = models.DateField(verbose_name="Дата начала")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    # Новые поля
    server_url = models.CharField(max_length=200, blank=True, verbose_name="Ссылка на сервере")
    sample_url = models.CharField(max_length=200, blank=True, verbose_name="Ссылка на размеры образцов")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    
    def __str__(self):
        return self.project_name
    
    @property
    def project_month(self):
        """Автоматически определяем месяц из даты создания"""
        return self.created_date.strftime('%Y-%m')
    
    @property
    def completion_percentage(self):
        total_stages = self.stages.count()
        if total_stages == 0:
            return 0
        
        completed_stages = self.stages.filter(status='completed').count()
        return int((completed_stages / total_stages) * 100)

class ProjectStage(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Не начат'),
        ('in_progress', 'В работе'),
        ('on_review', 'На проверке'),
        ('completed', 'Завершен'),
        ('blocked', 'Заблокирован'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stages', verbose_name="Проект")
    stage_name = models.CharField(max_length=200, verbose_name="Название этапа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name="Статус выполнения")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Кто выполняет")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Этап проекта"
        verbose_name_plural = "Этапы проектов"
    
    def __str__(self):
        return f"{self.project.project_name} - {self.stage_name}"