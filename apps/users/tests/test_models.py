# import pytest
# from ..models import CustomUserModel, UserRoleChoices
#
# test_user_data = {'email': '1@gmial.com', 'name': 'name_1', 'password': 'pass_1'}
#
#
# def test_create_employee(db):
#     user = CustomUserModel.objects.create_user(**test_user_data)
#
#     assert user.name == test_user_data['name']
#     assert user.email == test_user_data['email']
#     assert user.password != test_user_data['password']
#     assert user.role == UserRoleChoices.EMPLOYEE
#
#
# def test_create_restaurant_admin(db):
#     test_user_data['role'] = UserRoleChoices.RESTAURANT_ADMINISTRATOR
#     user = CustomUserModel.objects.create_user(**test_user_data)
#
#     assert user.name == test_user_data['name']
#     assert user.email == test_user_data['email']
#     assert user.password != test_user_data['password']
#     assert user.role == UserRoleChoices.RESTAURANT_ADMINISTRATOR
#
#
# def test_create_admin(db):
#     test_user_data['role'] = UserRoleChoices.ADMINISTRATOR
#     user = CustomUserModel.objects.create_superuser(**test_user_data)
#
#     assert user.name == test_user_data['name']
#     assert user.email == test_user_data['email']
#     assert user.password != test_user_data['password']
#     assert user.role == UserRoleChoices.ADMINISTRATOR
#
#
# def test_create_admin_with_wrong_role(db):
#     test_user_data['role'] = UserRoleChoices.EMPLOYEE
#     with pytest.raises(ValueError) as error:
#         CustomUserModel.objects.create_superuser(**test_user_data)
#
#     assert str(error.value) == 'User role has to be \'administrator\'.'
#
#
# def test_create_admin_with_wrong_active_status(db):
#     test_user_data['is_active'] = False
#     test_user_data['role'] = UserRoleChoices.ADMINISTRATOR
#     with pytest.raises(ValueError) as error:
#         CustomUserModel.objects.create_superuser(**test_user_data)
#
#     assert str(error.value) == 'User has to be active.'
