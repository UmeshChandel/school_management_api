from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
  page_size=5
  
  def get_paginated_response(self, data):
    return Response(
      {
        "current_page":self.page.number,
        "total_pages":self.page.paginator.num_pages,
        "total_data":self.page.paginator.count,
        "result":data
      }
    )