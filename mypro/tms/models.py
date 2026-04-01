from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Teacher(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('On Leave', 'On Leave'),
        ('Resigned', 'Resigned'),
    ]

    tname = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    leave_record = models.CharField(max_length=50, blank=True)
    
    # New Fields
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    cv_document = models.FileField(upload_to='cvs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.tname


class Users(models.Model):
    names = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'userss'



