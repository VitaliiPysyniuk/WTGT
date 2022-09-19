from rest_framework.serializers import ModelSerializer, ChoiceField
from django.contrib.auth import get_user_model

from .models import UserRoleChoices

UserModel = get_user_model()


class CustomChoiceField(ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class UserSerializer(ModelSerializer):
    role = CustomChoiceField(choices=UserRoleChoices.choices)

    class Meta:
        model = UserModel
        fields = '__all__'
        read_only_fields = ['is_active', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        user.save()

        return user


class UserUpdateSerializer(ModelSerializer):
    role = CustomChoiceField(choices=UserRoleChoices.choices)

    class Meta:
        model = UserModel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
