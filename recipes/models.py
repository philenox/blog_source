from django.db import models

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    ingredients = models.TextField()
    instructions = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'recipes'

class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=255)

    def __str__(self):
        return self.ingredient_name
    
    class Meta:
        app_label = 'recipes'

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name
    
    class Meta:
        app_label = 'recipes'

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'recipes'

class Instruction(models.Model):
    instruction_id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveIntegerField()
    instruction_text = models.TextField()

    class Meta:
        ordering = ['step_number']
        app_label = 'recipes'

    def __str__(self):
        return f"Step {self.step_number} for {self.recipe.title}"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.ingredient_name} for {self.recipe.title}"
    class Meta:
        app_label = 'recipes'

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tag.tag_name} for {self.recipe.title}"
    
    class Meta:
        app_label = 'recipes'