"""
Definition of forms.
"""

from django import forms
from app.models import Question, Choice, User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_text', 'subject', 'number_responses', 'correct_answer',)

class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('choice_text',)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email','nombre',)

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length = 254,
                               widget = forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'
                                    }))
    password = forms.CharField(label = _("Password"),
                               widget = forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'
                                   }))

class SubjectFilterForm(forms.Form):
    subjects = forms.ChoiceField(required=False, 
                                 label='Show subjects',
                                 # widget=forms.Select(attrs={'onchange': 'this.form.submit();'}), # On selection change, submit
                                 )

    def __init__(self, *args, **kwargs):
        super(SubjectFilterForm, self).__init__(*args, **kwargs)
        
        subjects_query = Question.objects.values_list('subject', flat=True).distinct()
        self.fields['subjects'].choices = [('', 'All')] + [(subject, subject) for subject in subjects_query]
