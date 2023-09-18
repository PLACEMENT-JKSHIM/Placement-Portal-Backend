from django.db import models
# Create your models here.
from home.models import Job
from student.models import Student


class Job_student(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'A'
        OFFERED = 'OF'
        REJECTED = 'R'
        PLACED = 'P'
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.APPLIED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('job', 'student')
    def __str__(self):
        return f"{self.job}-{self.student}-{self.status}"

    class Meta:
        unique_together = (('job', 'student'),)


class Notice(models.Model):
    title=models.CharField( max_length=60,null=False)
    content=models.TextField(null=False)
    hidden=models.BooleanField(default=False)
    created_on =models.DateTimeField( auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self):
         return f"{self.title}" 
    
class Statistic(models.Model):
    placed_count = models.IntegerField(default=0, verbose_name='Placed Count')
    offers_count = models.IntegerField(default=0, verbose_name='Offers Count')
    highest_ctc = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='Highest CTC')
    avg_ctc = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='Average CTC')
    median_ctc=models.DecimalField(max_digits=15, decimal_places=2, default=0.00, verbose_name='Median CTC')
    companies_visited = models.IntegerField(default=0, verbose_name='Companies Visited')
    def __str__(self):
        return f"Statistics"
    
class Job_branch(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    branch = models.ForeignKey('student.Branch', on_delete=models.CASCADE)
    class Meta:
        unique_together = (('job', 'branch'),)
    def __str__(self):
        return f"{self.job}-{self.branch}"