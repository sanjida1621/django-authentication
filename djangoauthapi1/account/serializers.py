from rest_framework import serializers
from account.models import User 

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields=['email','name','mobile','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }        
    #Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        mobile = attrs.get('mobile')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        if not mobile.startswith('01') or len(mobile) != 11:
            raise serializers.ValidationError(
                "Invalid Bangladeshi mobile number. Please enter a valid 11 digits mobile number starting with '01'."
            )
        return attrs
    #Registering User
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
  
  
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields=['email','password']
    
     
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','name', 'email', 'mobile']
        
        
        
class PasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)   
    class Meta:
        model = User
        fields=['password','password2']  
    #Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs
    
    
    
class SendResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            pass
        else:
            raise serializers.ValidationError("You are not a registered user")
        
        
        
class ResetPasswordSerializer(serializers.ModelSerializer):
       class Meta:
        model = User
        fields=['password','password2'] 