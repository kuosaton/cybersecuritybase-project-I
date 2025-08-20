from django.urls import path

from .views import indexView, addView, detailView, voteView, resultsView, deleteView

app_name = "polls"
urlpatterns = [
    path("", indexView, name="index"),
    path("add/", addView, name="add"),
    path("<int:pk>/", detailView, name="detail"),
    path("<int:pk>/vote/", voteView, name="vote"),
    path("<int:pk>/results/", resultsView, name="results"),
    path("<int:pk>/delete/", deleteView, name="delete"),
]
