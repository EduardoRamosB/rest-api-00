from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, CustomUserSerializer


class VolunteerListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRegistrationSerializer

    def get_queryset(self):
        print('VolunteerListCreateAPIView.get_queryset')
        return CustomUser.objects.filter(role='volunteer')

    def post(self, request, *args, **kwargs):
        print('VolunteerListCreateAPIView.post request.data:', request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        print('VolunteerListCreateAPIView.post user:', user)
        data = serializer.data
        print('VolunteerListCreateAPIView.post data:', data)
        return Response(data, status=status.HTTP_201_CREATED)


class VolunteerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        print('VolunteerRetrieveUpdateDestroyAPIView.get_queryset')
        return CustomUser.objects.filter(role='volunteer')


class UserRegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        print('UserRegistrationAPIView.post request.data:', request.data)

        serializer = self.get_serializer(data=request.data)
        print('UserRegistrationAPIView.post serializer:', serializer)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        print('UserRegistrationAPIView.post user:', user)
        token = RefreshToken.for_user(user)
        print('UserRegistrationAPIView.post token:', token)
        data = serializer.data
        print('UserRegistrationAPIView.post data:', data)
        data['tokens'] = {"refresh": str(token), "access": str(token.access_token)}

        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {"refresh": str(token), "access": str(token.access_token)}

        return Response(data, status=status.HTTP_200_OK)


class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
