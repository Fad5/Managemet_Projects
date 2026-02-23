# projects/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    USER_ROLES = [
        ('user', 'Обычный пользователь'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user', verbose_name="Роль")
    
    # Права для проектов
    can_create_projects = models.BooleanField(default=False, verbose_name="Может создавать проекты")
    can_edit_projects = models.BooleanField(default=False, verbose_name="Может редактировать проекты")
    can_delete_projects = models.BooleanField(default=False, verbose_name="Может удалять проекты")
    
    # Права для этапов
    can_create_stages = models.BooleanField(default=False, verbose_name="Может создавать этапы")
    can_edit_stages = models.BooleanField(default=False, verbose_name="Может редактировать этапы")
    can_delete_stages = models.BooleanField(default=False, verbose_name="Может удалять этапы")
    
    can_manage_users = models.BooleanField(default=False, verbose_name="Может управлять пользователями")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

# Создаем профиль автоматически при регистрации пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()

class Project(models.Model):
    project_name = models.CharField(max_length=100, unique=True, verbose_name="Название проекта")
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    
    # Новые поля
    server_url = models.CharField(max_length=200, blank=True, verbose_name="Ссылка на сервере")
    sample_url = models.CharField(max_length=200, blank=True, verbose_name="Ссылка на размеры образцов")
    
    # Кто создал проект
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_projects', verbose_name="Создатель")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    
    def __str__(self):
        return self.project_name
    
    @property
    def project_month(self):
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
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Этап проекта"
        verbose_name_plural = "Этапы проектов"
    
    def __str__(self):
        return f"{self.project.project_name} - {self.stage_name}"