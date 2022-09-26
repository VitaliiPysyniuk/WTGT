from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class RestaurantModel(models.Model):
    class Meta:
        db_table = 'restaurants'

    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=200)

    administrator = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True,
                                         related_name='restaurant')


class DishModel(models.Model):
    class Meta:
        db_table = 'dishes'

    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    price = models.FloatField(default=1.0)
    weight = models.IntegerField(default=1)

    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.CASCADE, related_name='dishes')


class MenuModel(models.Model):
    class Meta:
        db_table = 'menus'

    created_at = models.DateField(auto_now_add=True)

    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.CASCADE, related_name='menus')
    dishes = models.ManyToManyField(DishModel, related_name='menus')


class VoteModel(models.Model):
    class Meta:
        db_table = 'votes'
        unique_together = ['menu', 'user']

    voted_at = models.DateField(auto_now_add=True)

    menu = models.ForeignKey(MenuModel, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='votes')


