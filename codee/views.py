from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .utils import get_first_error
from .pydantic import *
from .response import Api_response
import logging
from pydantic import ValidationError 
from codee.serializers import studentserializer,Schoolserializer,Teacherserializer
# from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import Student,Teacher,School
from .services import *
from .pagination import CustomPagination
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
# # Create your views here.

# @api_view(['GET','POST'])
# def student_api(request):
#   if request.method=="GET":
#     student_obj=student.objects.all()
#     serializer=StudentSerializer(student_obj,many=True)
    
#     return Response(serializer.data)
  
#   if request.method=="POST":  
#     serializer=StudentSerializer(data=request.data)
    
#     if serializer.is_valid():
#       serializer.save
#       return Response(serializer.validated_data)
    
#     return Response(serializer.errors)
logger=logging.getLogger(__name__)

class student_api(APIView):
  def post(self,request):
    logger.info("Student create request received")
    
    try:
      data = request.data.dict() if hasattr(request.data,'dict') else dict(request.data)
      student_data=student_schema(**data)
      logger.info("Validation Successfull")
    except ValidationError as e:
      return Api_response.error_response(
        message="Validation Error",
        error=get_first_error(e)
      )  
    try:  
      student_m= Student_services.create_student(student_data)
      serializer =studentserializer(student_m)
      return Api_response.created(
        message="student Created",
        data=serializer.data
      )
    except Exception as e:
      logger.error(f"Unexpected error : {e}")  
      return Api_response.error_response(
        message="unexpected error",
        error="Cannot create new student"
      )


  def get(self,request,id=None):
    logger.info("REady retive student info")
    if id:
      try:
        student_obj=Student_services.get_student_by_id(id)
        serializer=studentserializer(student_obj)
        
        return Api_response.success_response(
          message="student infromation retrived",
          data=serializer.data
        )
      except Student.DoesNotExist as e:
        logger.info("Student data does not exist")
        return Api_response.not_found(
          message="Student not found",
          error=f"Student with id {id} does not exist"
        )    
    else:
      try:
        students=Student_services.get_all_students()
        
        paginator=Paginator(students,5)
        
        page_number=request.GET.get('page',1)
        
        page_obj=paginator.get_page(page_number)
        
        serializer=studentserializer(page_obj,many=True)
        
        return Api_response.success_response(
          message="Student data retrived",
          data={
            "current_page":page_obj.number,
            "number_of_pages":paginator.num_pages,
            "total_number_data":paginator.count,
            "student _result":serializer.data
          }
        )
      except Exception as e:
        logger.error(f"unexpected error : {e}")
        return Api_response.error_response(
          message="Data can't be fetched",
          error="Failed to retrive students"
        )     
        
  def put(self,request,id):
    logger.info("Ready to update details ")
    
    try:
      data = request.data.dict() if hasattr(request.data,'dict') else dict(request.data)
      print("GET:", request.GET)
      print("DATA:", request.data)
      student_obj=student_schema(**data)
    
      logger.info("validation successfull")
    except ValidationError as e:
      logger.error(f"Valisation error,{e}")
      return Api_response.error_response(
        message="Validation error",
        error=get_first_error(e)
      ) 
    try:   
      studentt=Student_services.update_student(id,student_obj)
      serializer=studentserializer(studentt)
      
      return Api_response.success_response(
        message="student information updated succesfully",
        data=serializer.data
      )
    except Student.DoesNotExist as e:  
      return Api_response.not_found(
        message="Student not found",
        error=f"Student with id {id} does not exist"
      )  
    except Exception as e:
      logger.error(f"Unexcpected error: {e}")
      return Api_response.error_response(
        message="Unexpected error",
        error="Something went wrong while updating the student"
      )  
      
  def delete(self,request,id):
    logger.info("ready to delete students")
    
    try:
       studentt=Student_services.delete_student_info(id)
       return Api_response.success_response(
         message="info is deleted "
       )  
    except Student.DoesNotExist as e:
      logger.error("Student does not exist",e)
      
      return Api_response.not_found(
        message="Student not found",
        error=f"Student with id {id} does not exist"
      )  
    except Exception as e:
      logger.info(f"unexpected error {e}")
      return Api_response.error_response(
        message="something went wrong",
        error="While deleting student info something went wrong"
      )     



class Schoolapi(APIView):
  def post(self,request):
    logger.info("school create request received")
    
    try:
      data = request.data.dict() if hasattr(request.data,'dict') else dict(request.data)
      school_data=school_schema(**data)
      logger.info("Validation Successfull")
    except ValidationError as e:
      return Api_response.error_response(
        message="Validation Error",
        error=get_first_error(e)
      ) 
    try:  
      school_s= School_services.createschool(school_data)
      serializer =Schoolserializer(school_s)
      return Api_response.created(
        message="school Created",
        data=serializer.data
      )
    except Exception as e:
      logger.error(f"Unexpected error : {e}")  
      return Api_response.error_response(
        message="unexpected error",
        error="Cannot create new school"
      )
  
  def get(self,request,id=None):
    logger.info("REady retive school info")
    if id:
      try:
        student_obj=School_services.get_school_by_id(id)
        serializer=Schoolserializer(student_obj)
        
        return Api_response.success_response(
          message="school infromation retrived",
          data=serializer.data
        )
      except School.DoesNotExist as e:
        logger.info("School data does not exist")
        return Api_response.not_found(
          message="School not found",
          error=f"School with id {id} does not exist"
        )    
    else:
      try:
        school =School_services.get_all_school()
        
        paginator=Paginator(school,5)
        
        page_number=request.GET.get('page',1)
        
        page_obj=paginator.get_page(page_number)
        
        serializer=Schoolserializer(page_obj,many=True)
        
        return Api_response.success_response(
          message="School data retrived",
          data={
            "current_page":page_obj.number,
            "number_of_pages":paginator.num_pages,
            "total_number_data":paginator.count,
            "student _result":serializer.data
          }
        )
      except Exception as e:
        logger.error(f"unexpected error : {e}")
        return Api_response.error_response(
          message="Data can't be fetched",
          error="Failed to retrive school data"
        )     
        
  def put(self,request,id):
    logger.info("Ready to update details ")
    
    try:
      data = request.data.dict() if hasattr(request.data,'dict') else dict(request.data)
      print("GET:", request.GET)
      print("DATA:", request.data)
      school_obj=school_schema(**data)
    
      logger.info("validation successfull")
    except ValidationError as e:
      logger.error(f"Valisation error,{e}")
      return Api_response.error_response(
        message="Validation error",
        error=get_first_error(e)
      ) 
    try:   
      school=School_services.update_school(id,school_obj)
      serializer=Schoolserializer(school)
      
      return Api_response.success_response(
        message="school information updated succesfully",
        data=serializer.data
      )
    except School.DoesNotExist as e:  
      return Api_response.not_found(
        message="School not found",
        error=f"School with id {id} does not exist"
      )  
    except Exception as e:
      logger.error(f"Unexcpected error: {e}")
      return Api_response.error_response(
        message="Unexpected error",
        error="Something went wrong while updating the school"
      )  
      
  def delete(self,request,id):
    logger.info("ready to delete students")
    
    try:
       studentt=School_services.delete_school(id)
       return Api_response.success_response(
         message="info is deleted "
       )  
    except School.DoesNotExist as e:
      logger.error("Student does not exist",e)
      
      return Api_response.not_found(
        message="School not found",
        error=f"School with id {id} does not exist"
      )  
    except Exception as e:
      logger.info(f"unexpected error {e}")
      return Api_response.error_response(
        message="something went wrong",
        error="While deleting school info something went wrong"
      )     



class Teacherapi(APIView):
  def post(self,request):
    logger.info("Teacher create request received")
    
    try:
      data = request.data.dict() if hasattr(request.data,'dict') else dict(request.data)
      teacher_data=Teacher_schema(**data)
      logger.info("Validation Successfull")
    except ValidationError as e:
      return Api_response.error_response(
        message="Validation Error",
        error=get_first_error(e)
      ) 
    try:  
      school_s= Teacher_services.create_teacher(teacher_data)
      serializer =Teacherserializer(school_s)
      return Api_response.created(
        message="Teacher is Created",
        data=serializer.data
      )
    except Exception as e:
      logger.error(f"Unexpected error : {e}")  
      return Api_response.error_response(
        message="unexpected error",
        error="Cannot create new teacher"
      )
  
  def get(self,request,id=None):
    logger.info("REady retive teacher info")
    if id:
      try:
        teacher_obj=Teacher_services.get_teacher_by_id(id)
        serializer=Teacherserializer(teacher_obj)
        
        return Api_response.success_response(
          message="teacher infromation retrived",
          data=serializer.data
        )
      except Teacher.DoesNotExist as e:
        logger.info("Teacher data does not exist")
        return Api_response.not_found(
          message="Teacher not found",
          error=f"Teacher with id {id} does not exist"
        )    
    else:
      try:
        teacher =Teacher_services.get_all_teachers()
        
        paginator=Paginator(teacher,5)
        
        page_number=request.GET.get('page',1)
        
        page_obj=paginator.get_page(page_number)
        
        serializer=Teacherserializer(page_obj,many=True)
        
        return Api_response.success_response(
          message="Teacher data retrived",
          data={
            "current_page":page_obj.number,
            "number_of_pages":paginator.num_pages,
            "total_number_data":paginator.count,
            "Teacher _result":serializer.data
          }
        )
      except Exception as e:
        logger.error(f"unexpected error : {e}")
        return Api_response.error_response(
          message="Data can't be fetched",
          error="Failed to retrive Teacher data"
        )     
        
  def put(self,request,id):
    logger.info("Ready to update details ")
    
    try:
      data = request.data.dict() if hasattr(request.data,'dict') else dict(request.data)
      print("GET:", request.GET)
      print("DATA:", request.data)
      teacher_data=Teacher_schema(**data)
    
      logger.info("validation successfull")
    except ValidationError as e:
      logger.error(f"Valisation error,{e}")
      return Api_response.error_response(
        message="Validation error",
        error=get_first_error(e)
      ) 
    try:   
      teacher=Teacher_services.update_teacher(id,teacher_data)
      serializer=Teacherserializer(teacher)
      
      return Api_response.success_response(
        message="teacher information updated succesfully",
        data=serializer.data
      )
    except Teacher.DoesNotExist as e:  
      return Api_response.not_found(
        message="Teacher not found",
        error=f"Teacher with id {id} does not exist"
      )  
    except Exception as e:
      logger.error(f"Unexcpected error: {e}")
      return Api_response.error_response(
        message="Unexpected error",
        error="Something went wrong while updating the Teacher"
      )  
      
  def delete(self,request,id):
    logger.info("ready to delete teacher")
    
    try:
       teacher=Teacher_services.deleting_teacher(id)
       return Api_response.success_response(
         message="info is deleted "
       )  
    except Teacher.DoesNotExist as e:
      logger.error("Teacher does not exist",e)
      
      return Api_response.not_found(
        message="Teacher not found",
        error=f"Teacher with id {id} does not exist"
      )  
    except Exception as e:
      logger.info(f"unexpected error {e}")
      return Api_response.error_response(
        message="something went wrong",
        error="While deleting Teacher info something went wrong"
      )     

    
      






















































































































class StudentListAPI(ListAPIView):
  def get_queryset(self):
    return Student_services.get_all_students()
  serializer_class = studentserializer
  paginaation_class = CustomPagination
  filter_backends=[
    DjangoFilterBackend,
    SearchFilter,
    OrderingFilter
  ]
  filterset_fields=["name","age"]
  search_fields=["name"]
  ordering_fields=["name","age"]
  