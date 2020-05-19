from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from .models import Doctor, Specialty, Review, Fword, ExceptionWord


class DoctorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "patronymic", "get_specs",)
    search_fields = ("first_name", "last_name", "patronymic", "spec__title",)
    list_filter = ("spec",)
    empty_value_display = '-пусто-'

    def get_specs(self, obj):
        return ", ".join([spec.title for spec in obj.spec.all()])


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "doctor", "review_text", "review_formatted_text", "created",)
    list_select_related = ("author", "doctor",)
    readonly_fields = ("text", "created")
    search_fields = ("doctor", "description",)
    empty_value_display = '-пусто-'

    def review_text(self, obj):
        return format_html_join(
            mark_safe('<br>'),
            '{}',
            ((line,) for line in obj.text.split('\n')),
        )
    def review_formatted_text(self, obj):
        return format_html_join(
            mark_safe('<br>'),
            '{}',
            ((line,) for line in obj.formatted_text.split('\n')),
        )


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Specialty)
admin.site.register(Fword)
admin.site.register(ExceptionWord)
