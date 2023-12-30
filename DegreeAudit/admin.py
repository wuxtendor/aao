from django.contrib import admin
from .models import UGMajor, Grade, Section, Course, SubjectLevel, SubjectCode, SubjectChoice


@admin.register(UGMajor)
class UGMajorAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )
    search_help_text = "Search by major name (eg. econ, Economics)"


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    search_fields = (
        "gpa",
    )
    search_help_text = "Search by GPA (eg. 3, ...)"


@admin.register(SubjectLevel)
class SubjectLevelAdmin(admin.ModelAdmin):
    search_fields = (
        "level",
    )
    search_help_text = "Search by subject level (eg. 101, 447, ...)"


@admin.register(SubjectCode)
class SubjectCodeAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )
    search_help_text = "Search by subject name (eg. ANT, SOC, ...)"


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "major"
    )
    list_filter = [
        "major"
    ]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = (
        "section",
        "subject_codes"
    )
    list_filter = [
        "section__major",
        "section__name",
        "passing_grade"
    ]


@admin.register(SubjectChoice)
class SubjectChoiceAdmin(admin.ModelAdmin):
    search_fields = (
        "subject_code__name",
        "levels__level",
        "course__section__name"
    )
    list_filter = [
        "course__section__major",
        "course__section__name",
        "course__passing_grade"
    ]
