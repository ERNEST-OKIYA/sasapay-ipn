from rest_framework.renderers import JSONRenderer
from rest_framework import status

class CustomJSONRenderer(JSONRenderer):
    """System wide custom renderer . this formats data for response 
    """
    
    def get_response_message(self,renderer_context):
        response=renderer_context.get('response')
        view = renderer_context['view']
        message,state='',''
        if not response:
            return [message,state]
        
        if response.status_code in [status.HTTP_200_OK,status.HTTP_201_CREATED,status.HTTP_202_ACCEPTED]:
           
            try:
                message = view.success_message
            except:
                message = "Success"
            state=True
        else:
            try:
                message = view.error_message
            except:
                message = "Sorry, request failed."
            state=False

        return [message,state]
    
        
    def render(self, data, accepted_media_type=None, renderer_context=None):
        message,state=self.get_response_message(renderer_context)    
        return super(CustomJSONRenderer, self).render(
            {'data': data,'message':message,'status':state}, accepted_media_type, renderer_context)
    