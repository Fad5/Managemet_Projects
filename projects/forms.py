# projects/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Project, ProjectStage, UserProfile
import re
from datetime import date

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })

class CustomUserCreationForm(UserCreationForm):
    # Убрали поле email
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.help_text = ''  # Убираем подсказки

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name', 
            'description',
            'server_url',
            'sample_url'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['description'].widget.attrs.update({'rows': 3})
        self.fields['server_url'].widget.attrs.update({
            'placeholder': 'Введите ссылку или текст'
        })
        self.fields['sample_url'].widget.attrs.update({
            'placeholder': 'Введите ссылку или текст'
        })

class ProjectStageForm(forms.ModelForm):
    class Meta:
        model = ProjectStage
        fields = ['stage_name', 'status', 'assigned_to', 'comment']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['stage_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название этапа'
        })
        
        self.fields['status'].widget.attrs.update({
            'class': 'form-control'
        })
        
        self.fields['assigned_to'].widget.attrs.update({
            'class': 'form-control'
        })
        
        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Добавьте комментарий к этапу'
        })
        
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)