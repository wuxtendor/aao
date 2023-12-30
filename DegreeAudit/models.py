from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UGMajor(models.Model):
    name = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "da_ug_major"


class Grade(models.Model):
    letter = models.CharField(primary_key=True, max_length=4)
    gpa = models.FloatField(null=False)

    def __str__(self):
        if self.letter == "none":
            return '-'
        return self.letter

    class Meta:
        db_table = "da_grade"


class SubjectLevel(models.Model):
    level = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.level.__str__()

    class Meta:
        db_table = "da_subject_level"


class SubjectCode(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "da_subject_code"


class Section(models.Model):
    name = models.CharField(max_length=500, null=False)
    description = models.TextField(default="", blank=True)
    credits = models.IntegerField(null=False)
    is_elective = models.BooleanField(null=False, default=False)
    major = models.ForeignKey(UGMajor, on_delete=models.DO_NOTHING)
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="uploads/")

    def save(self, *args, **kwargs):
        try:
            this = Section.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except: pass
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return f"({self.id}) {self.name} ({self.major.name})"

    class Meta:
        db_table = "da_section"


class Course(models.Model):
    course_number = models.IntegerField(null=False, default=1)
    passing_grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    subject_codes = models.ManyToManyField(SubjectCode)

    def __str__(self):
        codes = ",".join([subject_code.name for subject_code in self.subject_codes.all()])
        return f"({self.id}) {self.section.name}, {self.section.major.name} | {self.course_number} {codes}"

    class Meta:
        db_table = "da_course"


class SubjectChoice(models.Model):
    fixed = models.BooleanField(null=False, default=True)
    subject_code = models.ForeignKey(SubjectCode, on_delete=models.DO_NOTHING)
    levels = models.ManyToManyField(SubjectLevel, blank=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)

    def __str__(self):
        lvls = ",".join([level.__str__() for level in self.levels.all()])
        return f"({self.id}) {self.course.__str__()} | {self.subject_code.name} [{lvls}]"

    class Meta:
        db_table = "da_subject_choice"


class PassStatus(models.Model):
    status = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.status.capitalize()

    class Meta:
        db_table = "da_pass_status"


class StudentInfo(models.Model):
    created_date = models.DateField(default=timezone.now)
    student_id = models.CharField(max_length=9, null=False)
    student_name = models.CharField(max_length=200, null=False)
    student_surname = models.CharField(max_length=200, null=False)
    student_study_year = models.IntegerField(null=False)
    adviser = models.ForeignKey(User, on_delete=models.CASCADE)
    major = models.ForeignKey(UGMajor, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.student_id}, {self.student_name} {self.student_surname} "
                f"({self.student_study_year}, {self.major}) [{self.created_date}]")

    class Meta:
        db_table = "da_student_info"


class SectionInfo(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student_info = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    need_credits = models.IntegerField(null=False)

    class Meta:
        db_table = "da_section_info"


class CourseInfo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_info = models.ForeignKey(SectionInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = "da_course_info"


class SubjectChoiceInfo(models.Model):
    course_info = models.ForeignKey(CourseInfo, on_delete=models.CASCADE, null=True)
    section_info = models.ForeignKey(SectionInfo, on_delete=models.CASCADE, null=True)

    subject_code = models.CharField(max_length=100, null=False)
    subject_level = models.CharField(max_length=100, null=False)
    subject_name = models.CharField(max_length=500, null=False)
    subject_credit = models.IntegerField(null=False)
    subject_grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    pass_status = models.ForeignKey(PassStatus, on_delete=models.CASCADE)

    class Meta:
        db_table = "da_subject_choice_info"
