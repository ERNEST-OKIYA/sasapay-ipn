
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from rest_framework import generics

from mpesa import  settings
from utils.views import TransactionalViewMixin
from users.serializers import *
from users.models import User,Code




class UserList(TransactionalViewMixin,generics.ListCreateAPIView):
    """ used for user signup and listing users. to return only staff use: staff_only=true or give any variable. """
   
    serializer_class=UserSerializer
  
    
    filter_fields = ('first_name','last_name','email','groups','is_staff','is_superuser','groups',)
    
    search_fields=('first_name','last_name','email',)

    #authentication_classes = ()
    success_message='Successful'
    error_message="Failed"
    
    permission_classes = (AllowAny,)

    def perform_create(self,serializer):
        serializer.save()

    def get_queryset(self):
        user=self.request.user
        if user and user.is_authenticated():
            #return as per logged in user
            if user.is_superuser:
                return User.get_all()
            elif user.is_staff:
                return User.get_staff_and_normal()
        return User.objects.none()


    


class UserDetail(TransactionalViewMixin,generics.RetrieveUpdateDestroyAPIView):
    """ you can also mmake partial updates using PUT. 
    if password field is provided, the password will change. but no email/ notification will be sent to User
    regarding the changes
    """

    serializer_class=UserSerializer
    queryset=User.objects.all()

   
    
    def put(self, request, pk, format=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            valid_data = serializer.validated_data
            serializer.save()

            if valid_data.get('password'):
                user.set_password(valid_data.get('password'))
                user.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self,model_object):
        model_object.is_active=False
        model_object.is_deleted=True
        model_object.save()


 
   

    



class UserChangePassword(TransactionalViewMixin,generics.CreateAPIView):
    """To change password, 
    """
    
    serializer_class=UserChangePasswordSerializer
  
    error_message="All the fields are required"
    success_message="Your password was changed succesfully."
    
    
    def post(self, request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            valid_data=serializer.validated_data
            #chec if passwords match
            user=request.user

            old_password=valid_data.get('old_password')
            new_password=valid_data.get('new_password')
            new_password_again=valid_data.get('new_password_again')
            if new_password != new_password_again:
                #passwords do not match . fail
                self.error_message="Please enter the same password twice."
                raise serializers.ValidationError({'new_password':"Passwords do not match",
                                                   'new_password_again':"Passwords do not match"})
            
            #check if user with this password exists
            if not user.check_password(old_password):
                #not found
                self.error_message="Please enter your correct  password."
                raise serializers.ValidationError({'old_password':"Incorrect password"})
         
            #change password here also verify email if user is same.
            user.set_password(new_password)
            user.is_password_changed=True
          
            user.save()

            #send mail
            message='Password Changed Successfully'
            
            self.send_email(message=message,recipient=user.email,template_id=None,subject='Password Change')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    

    
    
class UserResetPassword(TransactionalViewMixin,generics.CreateAPIView):
    
    """
    Uses only POST
    email field is required.
    
    """
    
    serializer_class=UserResetPasswordSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    error_message="Oops something went wrong"
    success_message="Success"
    

    def post(self, request,format=None):
        serializer = UserResetPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            valid_data=serializer.validated_data
            email=valid_data.get('email')
            
            
            try:
                user=User.objects.get(email=email)
                reset_code  = self.get_reset_code()
                user.set_password(reset_code)
                self.send_default_pass(user,reset_code)
                user.is_password_changed=False
                user.save()
                self.success_message = "We sent you a temporary passcode."
                return Response(serializer.data)
            except User.DoesNotExist:
                self.error_message="Oops please check that your email is correct."
                raise serializers.ValidationError({'email':"User with this email Does not exist !"})
            except :
                self.error_message="Erro Occured."
                raise serializers.ValidationError('Please try again. Error occured.')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_reset_code(self):
        return  ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))


    def send_default_pass(self,user,reset_code):
        #message = 'fname:%s,password:%s' % (user.first_name,reset_code)
        message = 'Hi %s, Please use  %s as your temporary password.' % (user.first_name,reset_code)
        template_id = None #templates are for sendgrid 
        self.send_email(message=message, recipient=user.email, template_id=template_id,subject='Password Reset')
        if user.phone_number:
            self.send_sms(message,user.phone_number)

        return True



  

class UserVerifyEmail(TransactionalViewMixin,generics.ListCreateAPIView):
    """To verify email. For sending code, use GET for veification of the code received in email use POST
    For logged in users. 
    """
    
    serializer_class=UserVerifyEmailSerializer
    
    error_message="All the fields are required"
    success_message="Succesfully."
    
    def get_queryset(self):
        #send email verification code for looged in use 
        user=self.request.user
        code=Code.generate(user=user,reason=Code.EMAIL_VERIFICATION)
        message="Hi %s,\
        We received email verification request. Please enter %s to verify your email. \
        "%(user.first_name,code.code)

        self.send_email(message=message, recipient=user.email, template_id=None,subject='Verify Email')
        return []

    
    def post(self, request,format=None):
        serializer = UserVerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            valid_data=serializer.validated_data
            #chec if passwords match
            user=request.user

            verification_code=valid_data.get('verification_code')
            code=Code.is_valid(user=user,reason=Code.EMAIL_VERIFICATION,code=verification_code)
            if code:
                #valid 
                user.is_email_verified=True
                user.save()
                self.success_message="Email verified"
                #remove the Code
                code.delete()
            else:
                #incorrect options for verifying
                raise serializers.ValidationError({'verification_code':"The code is invalid."})
                self.error_message="Please enter correct code"
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserVerifyPhone(TransactionalViewMixin,generics.ListCreateAPIView):
    """To verify phone . For sending code, use GET for verification of the code received in sms use POST
    For logged in users. 
    """
    
    serializer_class=UserVerifyPhoneSerializer
    
    error_message="All the fields are required"
    success_message="Succesfully."
    
    def get_queryset(self):
        #send email verification code for looged in use 
        user=self.request.user
        code=Code.generate(user=user,reason=Code.PHONE_NUMBER_VERIFICATION)
        message="Hi %s,Please enter %s to verify your Phone Number."%(user.first_name,code.code)

        self.send_sms(message=message, recipient=user.phone_number)
        return []

    
    def post(self, request,format=None):
        serializer = UserVerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            valid_data=serializer.validated_data
            #chec if passwords match
            user=request.user

            verification_code=valid_data.get('verification_code')
            code=Code.is_valid(user=user,reason=Code.PHONE_NUMBER_VERIFICATION,code=verification_code)
            if code:
                #valid 
                user.is_phone_number_verified=True
                user.save()
                self.success_message="Phone number is verified."
                #remove the Code
                code.delete()
            else:
                #incorrect options for verifiyn
                raise serializers.ValidationError({'verification_code':"The code is invalid."})
                self.error_message="Please enter correct code"
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
