from django.shortcuts import render, get_object_or_404
from .models import Recipes, Tags

def recipe_index(request):
    selected_tags = request.GET.getlist('tags')
    tags = Tags.objects.using('recipes_db').all()
    
    if selected_tags:
        recipes = Recipes.objects.using('recipes_db').filter(
            recipe_tags__tag_id__in=selected_tags
        ).distinct()
    else:
        recipes = Recipes.objects.using('recipes_db').all()
    
    return render(request, 'recipe_index.html', {
        'recipes': recipes,
        'tags': tags,
        'selected_tags': list(map(int, selected_tags))
    })

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