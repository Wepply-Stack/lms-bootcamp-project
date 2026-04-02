from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework import status   
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Course
from .serializers import UserSerializer, LoginSerializer
from .permissions import IsAdminRole

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({"error": "Email and password are required", 
                        "details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    try:
        # Use email for login
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email or password"},
                        status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(username=user_obj.username,password=password)

    # No user
    if user is None:
        return Response({'error': 'Invalid email or password'}, 
                        status=status.HTTP_401_UNAUTHORIZED)
    
    # # Not admin/manager
    # if not user.is_staff:
    #     return Response({'detail': 'Forbidden'}, 
    #                     status=status.HTTP_403_FORBIDDEN)
    
    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key, "user":UserSerializer(user).data}, 
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_view(request):
    if hasattr(request.user,'auth_token'):
        request.user.auth_token.delete()

    return Response({"message": "Logged out successfully"}, 
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminRole])
def admin_dashboard(requst):
    total_courses = Course.objects.count()
    total_employees = User.objects.filter(is_staff=False).count()
    total_assignments = 20 # Check

    return Response({
        "total_courses": total_courses,
        "total_employees": total_employees,
        "total_assignments": total_assignments,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminRole])
def user_list(request):
    users = User.objects.filter(is_staff=False).order_by('id')

    return Response({
        "users": [
            {
                "id": user.id,
                "email": user.email,
                "role": "employee",
                "created_at": user.date_joined.isoformat().replace("+00:00", "Z")
            }
            for user in users
        ]   
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAdminRole])
def courses_view(request):
    if request.method == 'GET':
        courses = Course.objects.all().order_by('-created_at')
        return Response({
            "courses":[
                {
                    "id": course.id,
                    "title": course.title,
                    "description": course.description,
                    "status": course.status,
                    # Check
                    "created_at": course.created_at.isoformat().replace("+00:00", "Z")
                }
                for course in courses
            ]
        }, status = status.HTTP_200_OK)


    title = request.data.get('title')
    description = request.data.get('description')
    
    if not title:
        return Response({"error": "Title is required"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    course = Course.objects.create(
        title=title,
        description=description,
        status='draft' # Check 
    )

    return Response({
        "course": {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "status": course.status,
            # Check
            "created_at": course.created_at.isoformat().replace("+00:00", "Z")
        }
    }, status=status.HTTP_201_CREATED)



    # user = get_object_or_404(User, username=request.data['username'])
    # if not user.check_password(request.data['password']):
    #     return Response({"detail":'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    # token, _ = Token.objects.get_or_create(user=user)
    # serializer = UserSerializer(instance=user)
    # return Response({"token": token.key, "user":serializer.data})



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = User.objects.get(username=request.data['username'])
#         # Hashed password 
#         user.set_password(request.data['password'])
#         user.save()
#         token = Token.objects.create(user=user)
#         return Response({"token": token.key, "user":serializer.data})
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def test_token(request):
#     return Response("passed for {}".format(request.user.username))