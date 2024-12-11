from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    path("", views.IndexView.as_view(), name = "IndexView"),
    path("recipes/", views.RecipeList.as_view(), name = "recipe_list"),
    path("create/", views.CreateRecipe.as_view(), name = "recipe_create"),
    path("update/<int:pk>", views.UpdateRecipe.as_view(), name = "recipe_update"),
    path("delete/<int:pk>", views.DeleteRecipe.as_view(), name = "recipe_delete"),
    path("recipes/pdf", views.RecipeListPDF.as_view(), name = "recipe_list_pdf"),
    path("user/update/<int:pk>", views.UserProfile.as_view(), name = "user_update")
]