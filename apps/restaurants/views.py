from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction, models
from datetime import date
from dotenv import load_dotenv
import os
from django.http import HttpResponse

from .models import RestaurantModel, DishModel, MenuModel, VoteModel
from .serializers import RestaurantSerializer, DishSerializer, MenuSerializer, FullMenuSerializer, VoteSerializer
from ..users.permissions import IsAdmin, IsRestaurantAdmin, IsEmployee, IsAdminOfCertainRestaurantOrSystemAdmin
from ..users.models import UserRoleChoices
from .utils import parse_results, build_result_chart

load_dotenv('.env')


class RestaurantListCreateView(ListCreateAPIView):
    queryset = RestaurantModel.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsRestaurantAdmin]

    def post(self, request, *args, **kwargs):
        request.data['administrator'] = self.request.user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.request.user.role == UserRoleChoices.ADMINISTRATOR:
            return super().get_queryset()
        elif self.request.user.role == UserRoleChoices.RESTAURANT_ADMINISTRATOR:
            try:
                return self.queryset.filter(administrator_id=self.request.user.restaurant)
            except ObjectDoesNotExist:
                raise NotFound(detail='You haven\'t already created your restaurant or it was deleted.')


class RestaurantDestroyView(DestroyAPIView):
    queryset = RestaurantModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOfCertainRestaurantOrSystemAdmin]

    def get_object(self):
        filter = {
            'administrator': self.kwargs.get('restaurant_id')
        }

        return get_object_or_404(self.queryset, **filter)


class DishListCreateView(ListCreateAPIView):
    queryset = DishModel.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated, IsAdminOfCertainRestaurantOrSystemAdmin]

    def get_queryset(self):
        return self.queryset.filter(restaurant_id=self.kwargs.get('restaurant_id'))

    def post(self, request, *args, **kwargs):
        request.data['restaurant'] = kwargs.get('restaurant_id')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DishUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    queryset = DishModel.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated, IsAdminOfCertainRestaurantOrSystemAdmin]

    def get_object(self):
        filter = {
            'restaurant_id': self.kwargs.get('restaurant_id'),
            'id': self.kwargs.get('dish_id')
        }

        return get_object_or_404(self.queryset, **filter)


class MenuListCreateView(ListCreateAPIView):
    queryset = MenuModel.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsAdminOfCertainRestaurantOrSystemAdmin]

    def get_queryset(self):
        return self.queryset.filter(restaurant_id=self.kwargs.get('restaurant_id'))

    def get(self, request, *args, **kwargs):
        self.serializer_class = FullMenuSerializer
        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        request.data['restaurant'] = kwargs.get('restaurant_id')

        existing_menus = MenuModel.objects.all().filter(restaurant=kwargs.get('restaurant_id'), created_at=date.today())
        if len(existing_menus) != 0:
            raise ParseError(detail='You have already added the menu today.')

        menu_serializer = self.get_serializer(data=request.data)
        menu_serializer.is_valid(raise_exception=True)
        menu_serializer.save()

        return Response(menu_serializer.data, status.HTTP_201_CREATED)


class RestaurantMenuListView(ListAPIView):
    queryset = MenuModel.objects.all().order_by('id')
    serializer_class = FullMenuSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsEmployee]

    def get_queryset(self):
        return self.queryset.filter(created_at=date.today())


class VoteCreateView(ListAPIView, DestroyAPIView):
    queryset = VoteModel.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsEmployee]

    def get(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'menu': kwargs.get('menu_id')
        }

        existing_menus = MenuModel.objects.filter(id=kwargs.get('menu_id'), created_at=date.today())
        if len(existing_menus) == 0:
            raise ParseError(detail=f"There no menu with id: {kwargs.get('menu_id')} today.")

        votes = VoteModel.objects.filter(user_id=data['user'], voted_at=date.today())
        if len(votes) == 1:
            raise ParseError(detail='You have already voted today.')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

    def get_object(self):
        filter = {
            'user': self.request.user.id,
            'menu': self.kwargs.get('menu_id')
        }

        return get_object_or_404(self.queryset, **filter)


class VoteResultView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsEmployee]

    def get(self, request, *args, **kwargs):
        vote_results = VoteModel.objects.values('menu__restaurant_id', 'menu__restaurant__name').filter(
            menu__created_at=date.today()).annotate(votes=models.Count('id')).order_by('-votes')

        if len(vote_results) == 0:
            raise NotFound(detail='There are no votes yet.')

        mobile_app_version = request.headers.get('User-Agent').split('/')[1]

        if mobile_app_version > os.environ.get('MOBILE_APP_VERSION'):
            data = parse_results(vote_results)

            return Response(data, status.HTTP_200_OK)
        else:
            filepath = build_result_chart(vote_results)
            with open(f'{filepath}.png', "rb") as image:
                return HttpResponse(image.read(), content_type="image/png")
