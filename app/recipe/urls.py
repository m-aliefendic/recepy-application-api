"""
URL mappings for the recipe app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routes import DefailtRouter

from recipe import views

router = DefailtRouter()
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
