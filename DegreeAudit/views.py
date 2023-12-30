import base64
import os.path
import pdfkit

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import ObjectDoesNotExist
from django.template.loader import get_template
from django.conf import settings

from .models import (UGMajor, Grade, User, StudentInfo, SectionInfo, CourseInfo, Section,
                     PassStatus, Course, SubjectChoiceInfo)


def get_image_file_as_base64_data():
    with open(os.path.join(settings.BASE_DIR, 'uploads/logo.png'), 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()


logo = f'<img src="/uploads/logo.png" alt="Logo" style="width: 25.0%; height: 25.0%">'


def index(request):
    ug_programs = UGMajor.objects.all()
    return render(request, "../templates/index.html", context={"ug_programs": ug_programs, "logo": logo})


def audit(request, _id):
    ug_programs = UGMajor.objects.all()
    grades = Grade.objects.all()
    grades = grades[:len(grades) - 1]
    advisors = User.objects.filter(is_superuser=True).all()
    try:
        major = UGMajor.objects.get(id=_id)
    except ObjectDoesNotExist:
        return redirect("/")

    back = ('<br> '
            '<a href="/" class="btn btn-primary" style="margin-bottom: 10px">Back</a>')

    return render(request, "../templates/audit.html", context={"major": major, "grades": grades, "id_": _id,
                                                               "ug_programs": ug_programs, "advisors": advisors,
                                                               "logo": logo, "back": back})


def save_form(request, _id):
    if request.method == "POST":
        data = dict(request.POST.items())
        data.pop("csrfmiddlewaretoken")
        student_id = data.pop("studentId")
        student_name = data.pop("studentName")
        student_surname = data.pop("studentSurname")
        student_study_year = data.pop("studentStudyYear")
        adviser_username = data.pop("adviserId")
        major = data.pop("major")
        result = {}
        for k, v in data.items():
            k_split = k.split('-')
            if k_split[0] not in result:
                result[k_split[0]] = {}
            if k_split[1] not in result[k_split[0]]:
                result[k_split[0]][k_split[1]] = {}

            result[k_split[0]][k_split[1]][k_split[len(k_split) - 1]] = v

        new_student_info = StudentInfo(
            student_id=student_id,
            student_name=student_name,
            student_surname=student_surname,
            student_study_year=int(student_study_year),
            adviser=User.objects.get(username=adviser_username),
            major=UGMajor.objects.get(id=int(major))
        )
        new_student_info.save()

        new_sections = []
        new_courses = []
        new_subject_choices = []

        for section_id, course in result.items():
            new_section_info = SectionInfo(
                section=Section.objects.get(id=int(section_id)),
                student_info=new_student_info,
                need_credits=int(course.pop("credits")["credits"])
            )
            new_sections.append(new_section_info)
        new_sections = SectionInfo.objects.bulk_create(new_sections)

        for new_section in new_sections:
            for course_id, subject_choice_info in result[str(new_section.section.id)].items():
                if not new_section.section.is_elective:
                    new_course_info = CourseInfo(
                        course=Course.objects.get(id=int(course_id)),
                        section_info=new_section
                    )
                    new_courses.append(new_course_info)
        new_courses = CourseInfo.objects.bulk_create(new_courses)

        for new_section in new_sections:
            if new_section.section.is_elective:
                for course_id, subject_choice_info in result[str(new_section.section.id)].items():
                    new_subject_choice_info = SubjectChoiceInfo(
                        subject_code=subject_choice_info["course_code"].split('-')[0],
                        subject_level=subject_choice_info["course_level"],
                        subject_name=subject_choice_info["course_name"],
                        subject_credit=subject_choice_info["course_credit"],
                        subject_grade=Grade.objects.get(letter=subject_choice_info["course_grade"]),
                        pass_status=PassStatus.objects.get(status=subject_choice_info["passed"].lower()),
                        section_info=new_section
                    )
                    new_subject_choices.append(new_subject_choice_info)
            else:
                for new_course in new_courses:
                    if new_course.course.section.id == new_section.section.id:
                        subject_choice_info = result[str(new_section.section.id)][str(new_course.course.id)]
                        new_subject_choice_info = SubjectChoiceInfo(
                            subject_code=subject_choice_info["course_code"].split('-')[0],
                            subject_level=subject_choice_info["course_level"],
                            subject_name=subject_choice_info["course_name"],
                            subject_credit=subject_choice_info["course_credit"],
                            subject_grade=Grade.objects.get(letter=subject_choice_info["course_grade"]),
                            pass_status=PassStatus.objects.get(status=subject_choice_info["passed"].lower()),
                            course_info=new_course
                        )
                        new_subject_choices.append(new_subject_choice_info)

        SubjectChoiceInfo.objects.bulk_create(new_subject_choices)

        template = get_template('show.html')
        context = {"student": new_student_info, "logo": logo, "image": get_image_file_as_base64_data()}
        html = template.render(context)
        options = {
            "page-size": "a3",
            'encoding': "utf-8",
            "enable-local-file-access": ""
        }
        config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
        pdf = pdfkit.from_string(html, False, options, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="audit.pdf"'
        return response

    return redirect("/")


@login_required
def student_list(request):
    students = StudentInfo.objects.all()
    back = ('<br> '
            '<a href="/admin" class="btn btn-primary" style="margin-bottom: 10px">Back</a>')
    return render(request, "students_list.html", context={"students": students, "logo": logo, "back": back})


@login_required
def student_show(request, _id):
    student = StudentInfo.objects.get(id=_id)
    back = ('<br> '
            '<a href="/student_list/" class="btn btn-primary" style="margin-bottom: 10px">Back</a>')
    return render(request, "show.html", context={"student": student, "logo": logo, "back": back,
                                                 "image": get_image_file_as_base64_data()})
