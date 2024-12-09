from django.db import models

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Ingredients(models.Model):
    ingredient_id = models.AutoField(primary_key=True, blank=True)
    ingredient_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'Ingredients'


class Instructions(models.Model):
    instruction_id = models.AutoField(primary_key=True, blank=True)
    recipe = models.ForeignKey('Recipes', 
                               models.DO_NOTHING, 
                               blank=True, 
                               null=True,
                               related_name='instructions')
    step_number = models.IntegerField(blank=True, null=True)
    instruction_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'Instructions'


class Recipeingredients(models.Model):
    recipe = models.ForeignKey('Recipes', 
                               on_delete=models.DO_NOTHING,
                               primary_key=True,
                               related_name='recipe_ingredients',
                               blank=True)  # The composite primary key (recipe_id, ingredient_id) found, that is not supported. The first column is selected.
    ingredient = models.ForeignKey(Ingredients, 
                                   models.DO_NOTHING, 
                                   blank=True, 
                                   null=True,
                                   related_name='ingredient_recipes')
    amount = models.FloatField(blank=True, null=True)
    preparation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RecipeIngredients'


class Recipetags(models.Model):
    recipe = models.ForeignKey('Recipes', 
                                  on_delete=models.DO_NOTHING, 
                                  primary_key=True, 
                                  blank=True,
                                  related_name='recipe_tags')
    tag = models.ForeignKey('Tags', 
                            models.DO_NOTHING, 
                            blank=True, 
                            null=True,
                            related_name='tags_recipe')

    class Meta:
        managed = False
        db_table = 'RecipeTags'


class Recipes(models.Model):
    recipe_id = models.AutoField(primary_key=True, 
                                 blank=True)
    title = models.TextField()

    class Meta:
        managed = False
        db_table = 'Recipes'


class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True, 
                              blank=True)
    tag_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'Tags'