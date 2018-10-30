from django import forms
from django.contrib import messages
from permissions.templatetags.get_permissions import process_instruction, allocate_instruction
from .models import AmendmentsForRecord
from accounts.models import User, GeneralPracticeUser
from accounts import models


class MedicalReportFinaliseSubmitForm(forms.Form):
    prepared_and_signed = forms.ChoiceField(
        choices=AmendmentsForRecord.SUBMIT_OPTION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'finaliseChoice'}),
        required=False,
    )
    prepared_by = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': '', 'placeholder': '', 'readonly': True}),
        required=False,
    )
    gp_practitioner = forms.ModelChoiceField(queryset=None, required=False)
    instruction_checked = forms.BooleanField(required=False, initial=False, label='')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['gp_practitioner'] = forms.ModelChoiceField(queryset=user.get_query_set_within_organisation(), required=False)

    def is_valid(self, post_data):
        super().is_valid()
        if post_data['event_flag'] == 'submit' and not post_data['gp_practitioner']:
            self._errors = 'Please Enter Reviewer'
            return False

        if post_data['event_flag'] == 'submit' and 'prepared_and_signed' not in post_data:
            self._errors = 'Please Select Choice'
            return False

        if 'prepared_and_signed' in post_data:
            if post_data['prepared_and_signed'] == 'PREPARED_AND_REVIEWED' and not post_data['prepared_by']:
                self._errors = 'Please Enter Preparer'
                return False

        return True

    def clean(self):
        super().clean()
        if self.cleaned_data['prepared_and_signed'] == 'PREPARED_AND_SIGNED':
            self.cleaned_data['prepared_by'] = ''

        return self.cleaned_data


class AllocateInstructionForm(forms.Form):
    PROCEED_REPORT = 0
    ALLOCATE = 1
    RETURN_TO_PIPELINE = 2
    ALLOCATE_OPTIONS_CHOICE = (
        (PROCEED_REPORT, 'Proceed with report'),
        (ALLOCATE, 'Allocate to'),
        (RETURN_TO_PIPELINE, 'Return to pipeline view')
    )
    allocate_options = forms.ChoiceField(choices=ALLOCATE_OPTIONS_CHOICE, widget=forms.RadioSelect())
    gp_practitioner = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, user=None, instruction_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.type == models.GENERAL_PRACTICE_USER:
            organisation = user.userprofilebase.generalpracticeuser.organisation
            queryset = User.objects.filter(userprofilebase__generalpracticeuser__organisation=organisation)
            queryset = queryset.exclude(userprofilebase__generalpracticeuser__role=GeneralPracticeUser.PRACTICE_MANAGER)
            self.fields['gp_practitioner'] = forms.ModelChoiceField(queryset,
                                                                    required=False)
            if user and instruction_id:
                self.fields['allocate_options'] = self.set_allocate_by_permission(user, instruction_id, queryset)

    def set_allocate_by_permission(self, user, instruction_id, queryset):
        can_proceed = process_instruction(user.id, instruction_id)
        can_allocate = allocate_instruction(user.id)
        ALLOCATE_OPTIONS_CHOICE = [(self.RETURN_TO_PIPELINE, 'Return to pipeline view')]
        if can_allocate:
            ALLOCATE_OPTIONS_CHOICE.append((self.ALLOCATE, 'Allocate to'))
        else:
            self.fields['gp_practitioner'] = forms.ModelChoiceField(queryset, required=False, widget=forms.HiddenInput())
        if can_proceed:
            ALLOCATE_OPTIONS_CHOICE.append((self.PROCEED_REPORT, 'Proceed with report'))
        return forms.ChoiceField(choices=ALLOCATE_OPTIONS_CHOICE, widget=forms.RadioSelect())
