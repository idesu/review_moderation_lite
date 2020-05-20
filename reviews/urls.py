from django.urls import path
from . import views

urlpatterns = [
    path("add-review/<int:doctor_id>/", views.new_review, name="new_review"),
    path("reviews/", views.show_reviews, name="reviews"),
]
