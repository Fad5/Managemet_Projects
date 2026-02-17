# projects/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Project, ProjectStage
from datetime import date

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name', 
            'description',
            'server_url',
            'sample_url'
        ]
        # created_date убираем - будет auto_now_add=True
        # project_month убираем - будет вычисляться
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Для текстового поля
        self.fields['description'].widget.attrs.update({'rows': 3})
        
        # Просто текстовые поля для ссылок
        self.fields['server_url'].widget.attrs.update({
            'placeholder': 'Введите ссылку или текст'
        })
        
        self.fields['sample_url'].widget.attrs.update({
            'placeholder': 'Введите ссылку или текст'
        })
    
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        # Можно добавить проверку, что дата не в прошлом
        if start_date and start_date < date.today():
            # Можно предупредить, но не блокировать
            pass
        return start_date
    
class ProjectStageForm(forms.ModelForm):
    class Meta:
        model = ProjectStage
        fields = ['stage_name', 'status', 'assigned_to']
        widgets = {
            'stage_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название этапа'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
        

class ProjectStageForm(forms.ModelForm):
    class Meta:
        model = ProjectStage
        fields = ['stage_name', 'status', 'assigned_to']
        widgets = {
            'stage_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только активных пользователей в выпадающем списке
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)