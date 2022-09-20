from rest_framework.serializers import ModelSerializer

from .models import RestaurantModel, DishModel, MenuModel, MenuDishAssociateModel, VoteModel


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = RestaurantModel
        fields = '__all__'


class DishSerializer(ModelSerializer):
    class Meta:
        model = DishModel
        fields = '__all__'


class MenuDishAssociateSerializer(ModelSerializer):
    class Meta:
        model = MenuDishAssociateModel
        fields = '__all__'


class FullMenuDishAssociateSerializer(MenuDishAssociateSerializer):
    dish = DishSerializer(required=False)


class MenuSerializer(ModelSerializer):
    dishes = MenuDishAssociateSerializer(many=True, required=False)

    class Meta:
        model = MenuModel
        fields = '__all__'
        read_only_fields = ['created_at']


class FullMenuSerializer(MenuSerializer):
    dishes = FullMenuDishAssociateSerializer(many=True)
    restaurant = RestaurantSerializer()


class VoteSerializer(ModelSerializer):
    class Meta:
        model = VoteModel
        fields = '__all__'
