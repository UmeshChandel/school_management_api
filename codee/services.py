from .models import Student,School,Teacher


class School_services:
  @staticmethod
  def get_school_by_id(id):
    school_instance=School.objects.get(id=id)
    return school_instance
  
  @staticmethod
  def get_all_school():
    school_queryset=School.objects.all()
    return school_queryset
  @staticmethod
  def createschool(school_data):
    school=School.objects.create(name=school_data.name,address=school_data.address)
    return school
  
  @staticmethod
  def update_school(id,school_obj):
    school_instance=School.objects.get(id=id)
    school_instance.name=school_obj.name
    school_instance.address=school_obj.address
    school_instance.save()
    return school_instance
  
  @staticmethod
  def delete_school(id):
    school_instance=School.objects.get(id=id)
    school_instance.delete()

class Student_services:
  
  @staticmethod
  def get_student_by_id(id):
    try:
      student_instance=Student.objects.get(id=id)
      return student_instance ,"student fetched successfully"  
    except Student.DoesNotExist as e:
      return None ,"student not found"

  
  @staticmethod
  def get_all_students():
    student_queryset=Student.objects.all()
    print(type(student_queryset))
    return student_queryset
  
  @staticmethod
  def create_student(student_data):
    
    # /get school
    school =School.objects.get(id=student_data.school_id)
          
    student_obj=Student.objects.create(
      school=school,
      name=student_data.name,
      age=student_data.age
    )
    return student_obj 
  
  @staticmethod
  def update_student(id,student_obj):
    
    student_instance=Student.objects.get(id=id)
    
    student_instance.name=student_obj.name
    student_instance.age=student_obj.age
    
    student_instance.save()
    return student_instance
  @staticmethod
  def delete_student_info(id):
    student_instance=Student.objects.get(id=id)
    student_instance.delete() 
    
    
    
    
    
class Teacher_services:
  @staticmethod
  def get_teacher_by_id(id):
    teacher_instance=Teacher.objects.get(id=id)
    return teacher_instance
  
  @staticmethod
  def get_all_teachers():
    teacher_queryset=Teacher.objects.all()
    return teacher_queryset
  
  @staticmethod
  def create_teacher(teacher_data):
    # get school
    school=School.objects.get(id=teacher_data.school_id)
    
    teacher_obj=Teacher.objects.create(
      school=school,
      name=teacher_data.name ,
      subject=teacher_data.subject,
    )
    
    students=Student.objects.filter(id__in=teacher_data.student_id)
    
    teacher_obj.student.set(students)
    
    return teacher_obj
  
  @staticmethod
  def update_teacher(id,teacher_data):
    teacher=Teacher.objects.get(id=id)
    
    school=School.objects.get(id=teacher_data.school_id)
    
    teacher.name=teacher_data.name
    teacher.subject=teacher_data.subject
    teacher.school=school
    
    students=Student.objects.filter(id__in=teacher_data.student_id)
    teacher.student.set(students)
    
    teacher.save()
    return teacher
  
  @staticmethod
  def deleting_teacher(id):
    teacher=Teacher.objects.get(id=id)
    teacher.delete()
      
    
    
    
     