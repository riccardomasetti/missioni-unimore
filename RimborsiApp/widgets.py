from django import forms



class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/custom_clearable_file_input.html'

class PastiCustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/custom_clearable_file_input2.html'
