from rest_framework.response import Response
from rest_framework import status

class Api_response:
  
  @staticmethod
  def success_response(message,data=None):
    return Response(
      {
        "success":True,
        "message":message,
        "data":data
      },
      status=status.HTTP_200_OK
    )
  @staticmethod  
  def created(message,data=None):
    return Response(
      {
        "success":True,
        "message":message,
        "data":data
      },
      status=status.HTTP_201_CREATED
    )  
  @staticmethod  
  def error_response(message,error):
    return Response({
      "success":False,
      "message":message,
      "error":error
    },      
      status=status.HTTP_400_BAD_REQUEST                  
    )  
  
  @staticmethod
  def not_found(message,error):
    return Response(
      {
        "success":False,
        "message":message,
        "error":error
      },
      status=status.HTTP_404_NOT_FOUND
    )  

    