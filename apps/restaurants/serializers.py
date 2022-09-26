from rest_framework.serializers import ModelSerializer

from .models import RestaurantModel, DishModel, MenuModel, VoteModel


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = RestaurantModel
        fields = '__all__'


class DishSerializer(ModelSerializer):
    class Meta:
        model = DishModel
        fields = '__all__'


class MenuSerializer(ModelSerializer):
    class Meta:
        model = MenuModel
        fields = '__all__'
        extra_kwargs = {'created_at': {'read_only': True}}


class FullMenuSerializer(MenuSerializer):
    dishes = DishSerializer(many=True)
    restaurant = RestaurantSerializer()


class VoteSerializer(ModelSerializer):
    class Meta:
        model = VoteModel
        fields = '__all__'
