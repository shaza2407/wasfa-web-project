from django.urls import path
from . import views
from .views import add_recipe


urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('HomePage.html',views.homepage,name='homepage2'),
    path('register.html',views.register,name='register'),
    path('allrecipes_logged.html',views.allrecipes_logged,name='allrecipes_logged'),
    path('Meal_of_the_day.html',views.mealoftheday,name='meal of the day'),
    path('about.html',views.about,name='about'),
    path('login.html',views.login ,name='login'),
    path('userhomepage.html',views.userhomepage,name='user homepage'),
    path('adminhomepage.html',views.adminhomepage,name='admin homepage'),
    path('aboutadmin.html',views.aboutadmin,name='admin about'),
    path('aboutuser.html',views.aboutuser,name='user about'),
    path('add-recipe/', add_recipe, name='add_recipe'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('allrecepies-notlogged.html',views.allrecipes_notlogged,name='allrecipes_notlogged'),
    path('all-admin.html',views.all_admin,name='all_admin'),
    path('search/', views.search_form, name='search_form'),
    path('search-results/', views.search_results, name='search_results'),
    path('add-to-favorites/', views.AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('remove-from-favorites/', views.RemoveFromFavoritesView.as_view(), name='remove_from_favorites'),
    path('favorite_list.html', views.favorite_list, name='favorite_list'),
    path('user-recipes.html', views.user_recipes, name='user_recipes'),
    path('edit-recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete-recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]


