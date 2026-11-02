from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']  # 👈 fix here

from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'event_type', 'description', 'start_date', 'end_date',
            'time_info', 'location', 'mode', 'tags', 'registration_link', 'image'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event title (e.g. Cybersecurity Essentials)'}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter event summary/description'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 7:00 PM – 8:30 PM IST'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Online or Thoothukudi'}),
            'mode': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated: Cybersecurity, Zero Trust, Threat Detection'}),
            'registration_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }