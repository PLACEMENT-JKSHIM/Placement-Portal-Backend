from django.db import models
# Create your models here.
from home.models import Job
from student.models import Student


class Job_student(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'A'
        OFFERED = 'OF'
        REJECTED = 'R'
        QUALIFIED = 'Q'
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.REJECTED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('job', 'student')
    def is_eligible(self):
        if self.student.status != 'N':
            return False
        if self.job.status != 'O':
            return False
        if self.student.cgpa < self.job.curr_cgpa:
            return False
        if self.student.tenPercentage < self.job.sslc:
            return False
        if self.student.twelvePercentage < self.job.puc:
            return False
        elif self.student.diplomaPercentage < self.job.diploma:
            return False
        if self.student.degreePercentage > self.job.degree:
            return False
        if self.student.activeBacklog > self.job.max_activebacklog:
            return False
        if self.student.totalBacklog > self.job.max_histbacklog:
            return False
        if self.student.gap_edu > self.job.gap_edu:
            return False
        if self.student.dateOfBirth > self.job.min_dob:
            return False
        if self.student.dateOfBirth < self.job.max_dob:
            return False
        return True
    def __str__(self):
        return f"{self.job}-{self.student}-{self.status}"

class Notice(models.Model):
    title=models.CharField( max_length=60,null=False)
    content=models.CharField( max_length=1000,null=False)
    created_on =models.DateTimeField( auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self):
         return f"{self.title}" 