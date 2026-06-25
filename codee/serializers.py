from rest_framework import serializers
from .models import Student,School,Teacher


class SimpleSchoolSerializer(serializers.ModelSerializer):
   class Meta:
     model=School
     fields=['id','name','address']

class SimpleStudentSerailizer(serializers.ModelSerializer):
  class Meta:
    model=Student
    fields=['id','name','age']

class SimpleTeacherSerializer(serializers.ModelSerializer):
  class Meta:
    model=Teacher
    fields=['id','name','subject']         
   

class Schoolserializer(serializers.ModelSerializer):
  teachers=SimpleTeacherSerializer(many=True,source='teacher_set',read_only=True)
  class Meta:
    model=School
    fields=['id','name','address','teacher']

class studentserializer(serializers.ModelSerializer):
  school=SimpleSchoolSerializer(read_only=True)
  teacher=SimpleTeacherSerializer(source='teacher_set',read_only=True,many=True)
  class Meta:
    model=Student
    fields=['school','id','name','age','teacher']

class Teacherserializer(serializers.ModelSerializer):
  school=SimpleSchoolSerializer(read_only=True)
  student=SimpleStudentSerailizer(many=True,read_only=True) 
  class Meta:
    model=Teacher
    fields=['school','id','name','subject','student']
    

  
  