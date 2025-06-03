from modeltranslation.translator import register, TranslationOptions
from .models import Department, Job


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Job)
class JobTranslationOptions(TranslationOptions):
    fields = (
        'title', 
        'job_description', 
        'requirements'
    )