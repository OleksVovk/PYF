import random
from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from jedzonko.models import JedzonkoRecipe, JedzonkoPlan, JedzonkoRecipePlan, JedzonkoDayname


@method_decorator(csrf_exempt, name='dispatch')
class AddRecipeView(View):

    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):
        if request.method == "POST":
            try:
                name = request.POST['name']
                description = request.POST['description']
                preparation_time = request.POST['preparation_time']
                instruction = request.POST['instruction']
                ingredients = request.POST['ingredients']
                JedzonkoRecipe.objects.create(name=name, ingredients=ingredients, description=description,
                                              preparation_time=preparation_time, instruction=instruction)
                return render(request, 'app-add-recipe.html', {'err': 'Dodano przepis'})
            except (KeyError, ValueError):
                return render(request, 'app-add-recipe.html', {'err': 'Wypełnij formularz!!!'})
        return render(request, 'app-add-recipe.html')


class EditRecipeByIdView(View):

    def get(self, request):
        return render(request, 'app-edit-recipe.html')


@method_decorator(csrf_exempt, name='dispatch')
class AddPlanView(View):

    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        if request.method == "POST":
            try:
                name = request.POST['name']
                description = request.POST['description']
                if name == '' or description == '':
                    return render(request, 'app-add-schedules.html', {'err': 'Wypełnij formularz!!!'})
                JedzonkoPlan.objects.create(name=name, description=description)
                plan = JedzonkoPlan.objects.get(name=name)
                request.session['plan_id'] = plan.id
                return render(request, 'app-details-schedules.html')
            except (KeyError, ValueError):
                return render(request, 'app-add-schedules.html', {'err': 'Wypełnij formularz poprawnymi danymi!!!'})
        return render(request, 'app-add-schedules.html')


@method_decorator(csrf_exempt, name='dispatch')
class AddPlanDetailsView(View):

    def get(self, request):
        if request.session.get('plan_id'):
            plan = JedzonkoPlan.objects.get(id=request.session.get('plan_id'))
            session = request.session.get('plan_id')
            recipes = JedzonkoRecipe.objects.all()
            return render(request, 'app-schedules-meal-recipe.html', {'plan': plan, 'session': session,
                                                                      'recipes': recipes})
        raise PermissionDenied

    def post(self, request):
        if request.method == "POST":
            try:
                id_plan = request.POST['id_plan']
                if int(id_plan) == int(request.session.get('plan_id')):
                    meal_name = request.POST['meal_name']
                    order = request.POST['order']
                    recipename = request.POST['recipe']
                    dayname = request.POST['dayname']
                    recipe = JedzonkoRecipe.objects.get(name=recipename)
                    day_name = JedzonkoDayname.objects.get(day_name=dayname)
                    JedzonkoRecipePlan.objects.create(meal_name=meal_name, order=order, recipe_id_id=recipe.id,
                                                      plan_id_id=id_plan, day_name_id_id=day_name.id)
                    return HttpResponseRedirect(reverse('add-plan-details'))
                return Http404
            except (KeyError, ValueError):
                return render(request, 'app-schedules-meal-recipe.html', {'err': 'Wypełnij formularz poprawnymi danymi!!!'})
        return render(request, 'app-schedules-meal-recipe.html')

      
class MainPageView(View):

    def get(self, request):

        pool = list(JedzonkoRecipe.objects.all())
        random.shuffle(pool)
        recipes_list = pool[:3]
        return render(request, "index.html", {"recipes_list": recipes_list})


class DashboardView(View):

    def get(self, request):

        recipes_count = JedzonkoRecipe.objects.count()
        plans_count = JedzonkoPlan.objects.count()
        return render(request, "dashboard.html", {"recipes_count": recipes_count, "plans_count": plans_count})


class AboutView(View):

    def get(self, request):
        return render(request, "about.html")


class ContactView(View):

    def get(self, request):
        return render(request, "contact.html")


class RecipesView(View):
  
    def get(self, request):
        recipes_sorted = JedzonkoRecipe.objects.all().order_by('-votes', '-created')
        paginator = Paginator(recipes_sorted, 50)

        page = request.GET.get('page')
        recipes = paginator.get_page(page)

        return render(request, "app-recipes.html", {'recipes': recipes})


@method_decorator(csrf_exempt, name='dispatch')
class RecipeDetailsView(View):

    def get(self, request, **kwargs):
        if request.method == 'GET':
            try:
                idik = request.GET['id']
                recipe = JedzonkoRecipe.objects.get(id=idik)
                return render(request, "app-recipe-details.html", {'recipe': recipe})
            except KeyError:
                try:
                    idik = int(kwargs['id'])
                    recipe = JedzonkoRecipe.objects.get(id=idik)
                    return render(request, "app-recipe-details.html", {'recipe': recipe})
                except KeyError:
                    raise('Wystąpił błąd!')
        else:
            raise Http404

    def post(self, request, **kwargs):
        if request.method == "POST":
            idik = request.POST['id']
            chosen_recipe = JedzonkoRecipe.objects.get(id=idik)
            if request.POST.get("form_type") == 'form_one':
                chosen_recipe.votes += 1
                chosen_recipe.save()
                return redirect('recipe-details', idik)
            elif request.POST.get("form_type") == 'form_two':
                chosen_recipe.votes -= 1
                chosen_recipe.save()
                return redirect('recipe-details', idik)
        else:
            raise Http404


class PlansView(View):

    def get(self, request):
        plans_sorted = JedzonkoPlan.objects.all().order_by('name')
        paginator = Paginator(plans_sorted, 50)

        page = request.GET.get('page')
        plans = paginator.get_page(page)

        return render(request, "app-schedules.html", {'plans': plans})


class PlansDetailsView(View):

    def get(self, request, **kwargs):
        if request.method == 'GET':
            try:
                idik = request.GET['id']
                plan = JedzonkoPlan.objects.get(id=idik)
                return render(request, "app-details-schedules.html", {'plan': plan})
            except KeyError:
                try:
                    idik = int(kwargs['id'])
                    plan = JedzonkoPlan.objects.get(id=idik)
                    return render(request, "app-details-schedules.html", {'plan': plan})
                except KeyError:
                    raise ('Wystąpił błąd!')
        else:
            raise Http404





