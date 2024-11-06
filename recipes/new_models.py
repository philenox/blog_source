# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ingredients(models.Model):
    ingredient_id = models.AutoField(primary_key=True, blank=True, null=True)
    ingredient_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'Ingredients'


class Instructions(models.Model):
    instruction_id = models.AutoField(primary_key=True, blank=True, null=True)
    recipe = models.ForeignKey('Recipes', models.DO_NOTHING, blank=True, null=True)
    step_number = models.IntegerField(blank=True, null=True)
    instruction_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'Instructions'


class Recipeingredients(models.Model):
    recipe = models.OneToOneField('Recipes', models.DO_NOTHING, primary_key=True, blank=True, null=True)  # The composite primary key (recipe_id, ingredient_id) found, that is not supported. The first column is selected.
    ingredient = models.ForeignKey(Ingredients, models.DO_NOTHING, blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RecipeIngredients'


class Recipetags(models.Model):
    recipe = models.OneToOneField('Recipes', models.DO_NOTHING, primary_key=True, blank=True, null=True)  # The composite primary key (recipe_id, tag_id) found, that is not supported. The first column is selected.
    tag = models.ForeignKey('Tags', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RecipeTags'


class Recipes(models.Model):
    recipe_id = models.AutoField(primary_key=True, blank=True, null=True)
    title = models.TextField()

    class Meta:
        managed = False
        db_table = 'Recipes'


class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True, blank=True, null=True)
    tag_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'Tags'
