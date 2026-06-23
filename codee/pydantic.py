from pydantic import BaseModel,field_validator

class school_schema(BaseModel):
  name:str
  address:str
  
  @field_validator("name","address")
  @classmethod
  def validate_string(cls,value):
    value=value.strip()
    
    if not value:
      raise ValueError("Field cannot be empty")
    
    if value.isdigit():
      raise ValueError("Field cannot be only integers ")
    return value

class student_schema(BaseModel):
  name: str
  age: int
  school_id:int
  @field_validator("name")
  @classmethod
  def validate_string(cls,value):
    value=value.strip()
    if not value:
      raise ValueError("Field cannot be empty")
    
    if value.isdigit():
      raise ValueError("Name can not be only numbers")
    return value
    
  @field_validator("age")
  @classmethod
  
  def validate_integer(cls,value):
    if value<=0:
      raise ValueError("field cannot be zero or less than zero")
    return value
  

class Teacher_schema(BaseModel):
  name:str
  subject:str
  school_id: int
  student_id:list[int]
  
  @field_validator("name","subject")
  @classmethod
  def string_validator(cls,value):
    value=value.strip()
    
    if not value:
      raise ValueError("Field can not be empty")
    
    if value.isdigit():
      raise ValueError("Field can not be only integers")
    
    return value
  