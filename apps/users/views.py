from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer, UserUpdateSerializer
from .permissions import IsAdmin

UserModel = get_user_model()


class UserListView(ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        queryset = self.queryset
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        return queryset


class UserRegisterView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UserUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'id'


