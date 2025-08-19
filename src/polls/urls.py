from django.urls import path


from . import views
from .views import indexView, addView, detailView

app_name = "polls"
urlpatterns = [
    path("", indexView, name="index"),
    path("add/", addView, name="add"),
    path("<int:question_id>/", detailView, name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
