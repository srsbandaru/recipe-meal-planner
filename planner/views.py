from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from planner.models import Recipe
from django.urls import reverse_lazy
from planner.forms import RecipeForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
class IndexView(TemplateView):
    template_name = "planner/index.html"

class RecipeList(ListView):
    template_name = "planner/recipe_list.html"
    model = Recipe
    # queryset = Recipe.objects.all()
    context_object_name = "recipe_list"
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user).order_by("day_of_the_week", "meal_type")
        return queryset

class CreateRecipe(CreateView):
    template_name = "planner/recipe_form.html"
    model = Recipe
    success_url = reverse_lazy("planner:recipe_list")
    context_object_name = "form"
    http_method_names = ["get", "post"]
    fields = ["day_of_the_week", "meal_type", "recipe_name", "recipe_description"]

    def post(self, request):
        form = RecipeForm(request.POST)
        if not form.is_valid():
            context = {"form":form}
            return render(request, self.template_name, context)
        
        obj = form.save(commit = False)
        obj.user = self.request.user
        obj.save()

        messages.success(request, "Your recipe has been created successfully. ")
        return redirect(self.success_url)
    
class UpdateRecipe(UpdateView):
    template_name = "planner/recipe_form.html"
    model = Recipe
    success_url = reverse_lazy("planner:recipe_list")
    context_object_name = "form"
    http_method_names = ["get","post"]
    fields = ["day_of_the_week", "meal_type", "recipe_name", "recipe_description"]
    # form_class = RecipeForm

    def post(self, request, *args, **kwargs):
        recipe = get_object_or_404(self.model, id=self.kwargs["pk"])
        if recipe.user == self.request.user:
            form = RecipeForm(request.POST, instance=recipe)
            if not form.is_valid():
                context = {"form":form}
                return render(request, self.template_name, context)
            
            form.save()
            messages.success(request, "Your recipe has been updated successfully.")
        else:
            messages.error(request, "Your recipe has been not updated successfully.")
        
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(UpdateRecipe, self).get_context_data(**kwargs)
        context["form_type"] = "Update"
        return context

class DeleteRecipe(DeleteView):
    template_name = "planner/recipe_confirm_delete.html"
    model = Recipe
    context_object_name = "recipe"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("planner:recipe_list")
    http_method_names = ["get", "post"]

class RecipeListPDF(ListView):
    template_name = "planner/recipe_list_pdf.html"
    model = Recipe
    context_object_name = "recipe_list"
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user).order_by("day_of_the_week", "meal_type")
        return queryset
    
class UserProfile(UpdateView):
    template_name = "planner/user_form.html"
    model = User
    success_url = reverse_lazy("planner:recipe_list")
    context_object_name = "form"
    http_method_names = ["get","post"]
    fields = ["first_name", "last_name"]

    