from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from rest_framework.views import APIView

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        print(email)
        print(password)
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response({'message': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'id': user.id,
            'is_landlord': user.is_landlord,
            'is_admin': user.is_admin,
            'name': user.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=600),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # return Response({'jwt': token})
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
                'id': user.id,
                'is_landlord': user.is_landlord,
                'is_admin': user.is_admin,
                'name': user.name,
                'jwt': token
            }   
        return response
    

class UserView(APIView):
    def get(self, request):
        print(request.COOKIES)

        token = request.COOKIES.get('jwt')
        print(token)

        if not token:
            return Response({'error': 'JWT token not found in cookie'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'JWT token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
    
class ValidateView(APIView):
    def post(self, request):
        token = request.data['jwt']

        if not token:
            return Response({'error': 'JWT token not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'not authorized'}, 403)
        
        return Response(payload)
    
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'success'}
        return response