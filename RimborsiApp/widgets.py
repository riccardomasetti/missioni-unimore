from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import format_html


class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/custom_clearable_file_input.html'
    #template_name = 'django/forms/widgets/custom_clearable_file_input2.html'
    #template_name = 'django/forms/widgets/custom_clearable_file_input3.html'
    #template_name =  '/home/administrator/missioni-unimore/templates/widgets/custom_clearable_file_input.html'