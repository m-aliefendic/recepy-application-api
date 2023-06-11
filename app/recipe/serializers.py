"""
Serializers for recepe APIs
"""

from rest_framework import serializers

from core.model import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for receipes"""

    class Meta:
        model: Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']
