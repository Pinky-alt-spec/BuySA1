from home.models import Setting
from rest_framework import routers, serializers, viewsets
from product.models import Category


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
