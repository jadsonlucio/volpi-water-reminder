from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework import serializers

from water_reminder_api.models import UserAnatomy
from water_reminder_auth.models import UserAuthSession


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuthSession
        fields = ["auth_token", "refresh_token", "expiration_datetime"]


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    daily_goal_ml = serializers.SerializerMethodField(method_name="get_daily_goal")

    def to_representation(self, user):
        user_anatomy = UserAnatomy.objects.filter(user=user).first()
        if not user_anatomy:
            pass
        user.weight = user_anatomy.weight
        return super().to_representation(user)

    def create(self, validated_data):
        weight = validated_data.pop("weight")
        user = get_user_model()(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        UserAnatomy.objects.create(user=user, weight=weight)
        user.weight = weight

        return user

    def get_daily_goal(self, obj):
        return obj.weight * 35
