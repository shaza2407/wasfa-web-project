# forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient, Step

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'course_type', 'notes']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['order', 'description']

IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm, extra=1, can_delete=True)
StepFormSet = inlineformset_factory(Recipe, Step, form=StepForm, extra=1, can_delete=True)
