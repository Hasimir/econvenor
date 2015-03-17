from django import forms

from decisions.models import Decision


class MinutesDecisionForm(forms.ModelForm):

    def __init__(self, group, *args, **kwargs):
        super(MinutesDecisionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Decision

        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'charactercounter form-control',
                'maxlength': 300,
                'rows': 2,
                }),
            }

    def save(self, group, commit=True):
        decision = super(MinutesDecisionForm, self).save(commit=False)
        decision.group = group
        if commit:
            decision.save()
        return decision
