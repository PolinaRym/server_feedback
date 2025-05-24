from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'description', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Опишите ваше обращение'
            }),
            'feedback_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['attachment'].widget.attrs.update({'class': 'form-control'})

    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment:
            if attachment.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError('Размер файла не должен превышать 10MB')
        return attachment