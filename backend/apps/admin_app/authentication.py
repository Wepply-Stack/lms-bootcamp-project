from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that ensures the user exists and is active.
    """
    
    def authenticate(self, request):
        try:
            result = super().authenticate(request)
            
            if result is None:
                return None
            
            user, validated_token = result
            
            user_id = validated_token.get('user_id')
            role = validated_token.get('role')
            
            if user.id != user_id:
                raise InvalidToken('User ID mismatch')
            
            if not hasattr(user, 'role') or user.role != role:
                user.role = role
            
            return (user, validated_token)
            
        except InvalidToken as e:
            raise exceptions.AuthenticationFailed(str(e))
        except TokenError as e:
            raise exceptions.AuthenticationFailed('Token is invalid or expired')
        except Exception as e:
            raise exceptions.AuthenticationFailed('Authentication failed')