from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class SignupView(APIView):
    """
    API endpoint for user signup.
    Expects POST data with 'username', 'email' (optional), and 'password'.
    Returns a token and user data on successful registration.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create a token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    API endpoint for user login.
    Expects POST data with 'username' and 'password'.
    Returns a token and basic user info on successful login.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)  # Creates a session (optional if using only tokens)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """
    API endpoint for user logout.
    Requires token authentication.
    Deletes the user's token, effectively logging them out.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Optionally, if you're using session-based auth, you could call logout(request)
        try:
            request.user.auth_token.delete()
        except Exception as e:
            return Response({'error': 'Token deletion failed.'}, status=status.HTTP_400_BAD_REQUEST)
        logout(request)  # Optional: logs out from session if using session auth.
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
