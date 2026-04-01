import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication class that extracts and validates JWT tokens
    from the Authorization header.
    """
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        try:
            # Extract token from Bearer scheme
            token_type, token = auth_header.split()
            
            if token_type.lower() != 'bearer':
                raise exceptions.AuthenticationFailed(
                    'Invalid token type. Use Bearer token.'
                )
                
        except ValueError:
            raise exceptions.AuthenticationFailed(
                'Invalid Authorization header format. Use: Bearer <token>'
            )
        
        try:
            # Decode and validate token
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            
            user_id = payload.get('user_id')
            role = payload.get('role')
            
            if not user_id or not role:
                raise exceptions.AuthenticationFailed(
                    'Invalid token payload'
                )
            
            # Get user from database
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')
            
            # Attach additional data to user object
            user.role = role
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

