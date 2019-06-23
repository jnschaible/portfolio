from django.urls import path
from . import views


urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("tag/<category>/", views.blog_category, name="blog_category"),
    path("author/<author>/", views.blog_author, name="blog_author"),
    path("about_me/", views.about_me, name="about_me")
]
