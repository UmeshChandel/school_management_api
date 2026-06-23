from django.db import models

# Create your models here.
class School(models.Model):
  name=models.CharField(max_length=20)
  address=models.CharField(max_length=20)
  
  
  def __str__(self):
    return self.name
  
class Student(models.Model):
  school=models.ForeignKey(School,on_delete=models.CASCADE)
  name=models.CharField(max_length=10)
  age=models.IntegerField() 
  def __str__(self):
    return f"{self.name}, {self.school.name}"
  
class Teacher(models.Model):
  school=models.ForeignKey(School,on_delete=models.CASCADE)
  student=models.ManyToManyField(Student)
  name=models.CharField(max_length=10)
  subject=models.CharField(max_length=10)
  
  def __str__(self):
    return f"{self.name}, {self.school.name}"
 

  