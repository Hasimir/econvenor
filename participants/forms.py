from django import forms

from django.utils.translation import ugettext, ugettext_lazy as _

from participants.models import Participant
from tasks.models import Task

class AddParticipantForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(AddParticipantForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Participant
        fields = ['first_name',
                  'last_name',
                  'email',
                  'phone',
                  'notes',
                  ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
                }),
            'email': forms.EmailInput(attrs={
                'class': 'charactercounter form-control',
                }),
            'phone': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
                }),
            'notes': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 300,
                'rows': 4,
                }),
            }

    def save(self, group, commit=True):
        participant = super(AddParticipantForm, self).save(commit=False)
        participant.group = group
        if commit:
            participant.save()
        return participant


class EditParticipantForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(EditParticipantForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Participant
        fields = ['first_name',
                  'last_name',
                  'email',
                  'phone',
                  'status',
                  'reminders',
                  'notes',
                  ]
        labels = {
            'reminders': _('Automatically email reminders about nearly-due and overdue tasks (recommended)'),
                }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
                }),
            'email': forms.EmailInput(attrs={
                'class': 'charactercounter form-control',
                }),
            'phone': forms.TextInput(attrs={
                'class': 'charactercounter form-control',
                }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                }),
            'notes': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 300,
                'rows': 4,
                }),
            }

    def save(self, group, commit=True):
        participant = super(EditParticipantForm, self).save(commit=False)
        participant.group = group
        if commit:
            participant.save()
        return participant


class MyTasksForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['completion_date']

    def save(self, commit=True):
        task = super(MyTasksForm, self).save(commit=False)
        task.participant_set_status_completed = True
        task.status = 'Completed'
        if commit:
            task.save()
        return task
