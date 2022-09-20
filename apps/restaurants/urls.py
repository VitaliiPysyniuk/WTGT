from django.urls import path

from .views import RestaurantListCreateView, RestaurantDestroyView, DishListCreateView, DishUpdateDestroyView, \
    MenuListCreateView, RestaurantMenuListView, VoteCreateView, VoteResultView

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='get_create_restaurants'),
    path('/<int:restaurant_id>', RestaurantDestroyView.as_view(), name='delete_restaurant'),
    path('/<int:restaurant_id>/dishes', DishListCreateView.as_view(), name='get_create_restaurant_dishes'),
    path('/<int:restaurant_id>/dishes/<int:dish_id>', DishUpdateDestroyView.as_view(),
         name='update_delete_restaurant_dishes'),
    path('/<int:restaurant_id>/menus', MenuListCreateView.as_view(), name='get_create_restaurant_menus'),
    path('/menus', RestaurantMenuListView.as_view(), name='get_daily_menus_of_all_restaurants'),
    path('/menus/<int:menu_id>/vote', VoteCreateView.as_view(), name='vote_for_menu'),
    path('/menus/vote-results', VoteResultView.as_view(), name='get_vote_results')
]
