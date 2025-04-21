from django.shortcuts import render,redirect, get_object_or_404
from .models import user, Recipe
from django.contrib import messages  
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .forms import RecipeForm, IngredientFormSet, StepFormSet
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Recipe, UserFavorite
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User





def homepage(request):
    return render(request,'parts/HomePage.html')

def userhomepage(request):
    return render(request,'parts/userhomepage.html')

def adminhomepage(request):
    return render(request,'parts/adminhomepage.html')

def aboutadmin(request):
    return render(request,'parts/aboutadmin.html')

def aboutuser(request):
    return render(request,'parts/aboutuser.html')

def allrecipes_notlogged(request):
    recipes = Recipe.objects.all()
    return render(request,'parts/allrecipes-notlogged.html', {'recipes': recipes})

def allrecipes_logged(request):
    recipes = Recipe.objects.all()
    return render(request,'parts/allrecipes-logged.html', {'recipes': recipes})

def all_admin(request):
    recipes = Recipe.objects.all()
    return render(request,'parts/all-admin.html', {'recipes': recipes})

def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'parts/recipe_detail.html', {'recipe': recipe})

def mealoftheday(request):
    return render(request,'parts/Meal_of_the_day.html')

def about(request):
    return render(request,'parts/about.html')


def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        username = request.POST.get('username')
        is_admin = request.POST.get('is_admin') == 'on'

        if not all([email, password, username, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, 'parts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return render(request, 'parts/register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'parts/register.html')

        # Create the user using Django's create_user method
        user_instance = User.objects.create_user(username=username, email=email, password=password)
        
        # Set is_admin flag if needed
        if is_admin:
            user_instance.is_staff = True
            user_instance.is_superuser = True
            user_instance.save()

        messages.success(request, "Registration successful. Please log in.")
        return redirect('/login.html')

    return render(request, 'parts/register.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return render(request, 'parts/login.html')

        user_instance = User.objects.filter(email=email).first()
        if user_instance is not None:
            user = authenticate(request, username=user_instance.username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_staff:
                    return redirect('/adminhomepage.html')
                else:
                    return redirect('/userhomepage.html')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
        
    return render(request, 'parts/login.html')

@login_required
def add_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredients')
        step_formset = StepFormSet(request.POST, prefix='steps')

        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user  # Associate the recipe with the logged-in user
            recipe.save()
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()
            steps = step_formset.save(commit=False)
            for step in steps:
                step.recipe = recipe
                step.save()
            return redirect('/user-recipes.html')  # Redirect to the user's recipes page
    else:
        recipe_form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
        step_formset = StepFormSet(prefix='steps')

    return render(request, 'parts/add_recipe.html', {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
    })


def search_form(request):
    return render(request, 'parts/search.html')

def search_results(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(name__icontains=query)
    else:
        recipes = Recipe.objects.all()
    return render(request, 'parts/search_results.html', {'recipes': recipes, 'query': query})



class AddToFavoritesView(View):
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            recipe_id = data.get('recipe_id')
            if recipe_id is None:
                return JsonResponse({'status': 'error', 'message': 'No recipe ID provided'})
            try:
                recipe = Recipe.objects.get(id=recipe_id)
                UserFavorite.objects.get_or_create(user=request.user, recipe=recipe)
                return JsonResponse({'status': 'success', 'message': 'Recipe added to favorites'})
            except Recipe.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Recipe not found'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})

class RemoveFromFavoritesView(View):
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            recipe_id = data.get('recipe_id')
            if recipe_id is None:
                return JsonResponse({'status': 'error', 'message': 'No recipe ID provided'})
            try:
                recipe = Recipe.objects.get(id=recipe_id)
                favorite = UserFavorite.objects.filter(user=request.user, recipe=recipe)
                if favorite.exists():
                    favorite.delete()
                    return JsonResponse({'status': 'success', 'message': 'Recipe removed from favorites'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Favorite not found'})
            except Recipe.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Recipe not found'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})

@login_required
def favorite_list(request):
    favorites = UserFavorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'parts/favorite_list.html', {'favorites': favorites})




@login_required
def user_recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'parts/user_recipes.html', {'recipes': recipes})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(request.POST, instance=recipe, prefix='steps')

        if recipe_form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe_form.save()
            ingredient_formset.save()
            step_formset.save()
            return JsonResponse({'status': 'success', 'message': 'Recipe updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'There was an error with the form'})
    else:
        recipe_form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(instance=recipe, prefix='steps')

    return render(request, 'parts/edit_recipe.html', {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'recipe': recipe
    })

@csrf_exempt
@login_required
def delete_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
        recipe.delete()
        return JsonResponse({'status': 'success', 'message': 'Recipe deleted successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




