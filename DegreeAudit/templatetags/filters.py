from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def int_range(i):
    return range(i)


@register.filter
def get_name(s: str):
    lines = s.split("_")
    return " ".join([l.capitalize() for l in lines])


@register.filter
def get_len(l: list):
    return len(l)


@register.filter
def get_elem(l: list, i: int):
    if l.__len__() <= 0:
        return None
    return l[i]


@register.filter
def get_all(q):
    return q.all()


@register.simple_tag
def increment(v):
    return v + 1


@register.filter
def get_elective_len(cs):
    return cs // 6


@register.filter
def get_total_credits(student_info):
    total_credits = 0
    for section_info in student_info.sectioninfo_set.all():
        if not section_info.section.is_elective:
            for course_info in section_info.courseinfo_set.all():
                for subject_choice_info in course_info.subjectchoiceinfo_set.all():
                    if subject_choice_info.pass_status.status == "pass":
                        total_credits += subject_choice_info.subject_credit
        else:
            for subject_choice_info in section_info.subjectchoiceinfo_set.all():
                if subject_choice_info.pass_status.status == "pass":
                    total_credits += subject_choice_info.subject_credit

    return total_credits
