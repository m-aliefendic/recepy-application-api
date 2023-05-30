"""
Test gor recipe APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework import APIClient

from core.models import Recipe

from recepi.serializers import RecepiSerializer

RECEPI_URL = reverse('recipe:recipe-list')


def create_recipe(user, **params):
    """Create and return sample recipe."""
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'decription': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.clinet = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(RECEPI_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    """Test authenticated APi requests."""

    def setUp(self):
        self.clinet = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECEPI_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serilaizer = RecepiSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilaizer.data)

    def test_recope_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECEPI_URL)
        recipes = Recipe.objects.filter(uder=self.user).order_by('-id')
        serilaizer = RecepiSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilaizer.data)
