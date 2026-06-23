from rest_framework import serializers
from .models import Student,School,Teacher


class Schoolserializer(serializers.ModelSerializer):
  class Meta:
    model=School
    fields='__all__'


class studentserializer(serializers.ModelSerializer):
  school=Schoolserializer(read_only=True)
  class Meta:
    model=Student
    fields= '__all__'

class Teacherserializer(serializers.ModelSerializer):
  school=Schoolserializer(read_only=True)
  student=studentserializer(many=True,read_only=True)
  
  class Meta:
    model=Teacher
    fields='__all__'    

    

  
  