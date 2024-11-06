from django.shortcuts import render, get_object_or_404
from .models import Recipes

def recipe_index(request):
    recipes = Recipes.objects.using('recipes_db').all()
    return render(request, 'recipe_index.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipes.objects.using('recipes_db'), recipe_id=recipe_id)
    instructions = recipe.instructions.all()
    ingredients = recipe.recipe_ingredients.all()
    tags = recipe.recipe_tags.all()
    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'instructions': instructions,
        'ingredients': ingredients,
        'tags': tags
    })