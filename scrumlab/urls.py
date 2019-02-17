"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path

from jedzonko.views import AddRecipeView, EditRecipeByIdView, AddPlanView, AddPlanDetailsView, AboutView, \
    ContactView, RecipesView, MainPageView, DashboardView, RecipeDetailsView, PlansView, PlansDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipe/add/', AddRecipeView.as_view(), name='add-recipe'),
    path('recipe/modify/1/', EditRecipeByIdView.as_view(), name='edit-recipe-by-id'),
    path('plan/add/', AddPlanView.as_view(), name='add-plan'),
    path('plan/add/details/', AddPlanDetailsView.as_view(), name='add-plan-details'),
    path('', MainPageView.as_view(), name='main_page'),
    path('main/', DashboardView.as_view(), name='dash_board'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('recipe/list/', RecipesView.as_view(), name='recipe-list'),
    re_path(r'^recipe/details/(?P<id>(\d)+)/$', RecipeDetailsView.as_view(), name='recipe-details'),
    path('plan/list/', PlansView.as_view(), name='plan-list'),
    path('recipe/list/add_recipe', AddRecipeView.as_view(), name='add-recipe-from-list'),
    re_path(r'^plan/details/(?P<id>(\d)+)/$', PlansDetailsView.as_view(), name='plan-details'),

]
