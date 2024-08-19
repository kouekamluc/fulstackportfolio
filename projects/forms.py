
from django import forms
from .models import Project, ProjectImage
from taggit.forms import TagWidget

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']  # Exclude user from the form
        fields = ['title', 'description', 'start_date', 'end_date', 'github_link', 'live_link', 'tags']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Enter tags separated by commas'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'tags':
                self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

ProjectImageFormSet = forms.inlineformset_factory(
    Project, ProjectImage, form=ProjectImageForm,
    extra=1, can_delete=True
)