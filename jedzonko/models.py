from django.db import models


# Create your models here.

class JedzonkoPage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)


class JedzonkoPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class JedzonkoRecipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField(null=True)
    votes = models.IntegerField(default=0)


class JedzonkoDayname(models.Model):
    day_name = models.CharField(max_length=16)
    order = models.AutoField

    # DODANIE DNI TYGODNIA DO BAZY

    # from jedzonko.models import JedzonkoDayname
    # day_names = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
    # for day in day_names:
    #   JedzonkoDayname.objects.create(day_name=day)


class JedzonkoRecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    recipe_id = models.ForeignKey('JedzonkoRecipe', on_delete=models.CASCADE)
    plan_id = models.ForeignKey('JedzonkoPlan', on_delete=models.CASCADE)
    day_name_id = models.ForeignKey('JedzonkoDayname', on_delete=models.CASCADE)
