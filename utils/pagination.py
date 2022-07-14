from rest_framework.response import Response
from rest_framework import pagination



class CustomPageNumberPagination(pagination.PageNumberPagination):

    page_size_query_param = 'page_size' #used in get rquest filtering i.e ?page_size=2 
    # Set to an integer to limit the maximum page size the client may request.
    max_page_size = None
    

    def get_page_link(self,page_number): #get full link url for given page. 
        url = self.request.build_absolute_uri()
        return pagination.replace_query_param(url, self.page_query_param, page_number)

  
   
    def get_paginated_response(self, data):
        return Response({
            'pagination':{
                'count': self.page.paginator.count,
                'num_pages': self.page.paginator.num_pages,
                'current_page':self.page.number,
              
                'html_context':{
                                'previus_url':self.get_html_context().get('previous_url'),
                                'next_url':self.get_html_context().get('next_url'),
                                'page_links':[ {'url':p[0],'number':p[1],'is_active':p[2],'is_break':p[3] } for p in self.get_html_context().get('page_links')]
                },
                'start_index':self.page.start_index(),
                'end_index':self.page.end_index(),
            },
            'results': data
        })