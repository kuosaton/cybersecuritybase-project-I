from django.urls import path


from . import views
from .views import indexView, addView, detailView, voteView, deleteView

app_name = "polls"
urlpatterns = [
    path("", indexView, name="index"),
    path("add/", addView, name="add"),
    path("<int:pk>/", detailView, name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:pk>/vote/", voteView, name="vote"),
    path("<int:pk>/delete/", deleteView, name="delete"),
]
