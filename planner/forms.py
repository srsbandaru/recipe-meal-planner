from django.forms import ModelForm

from planner.models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["day_of_the_week", "meal_type", "recipe_name", "recipe_description"]