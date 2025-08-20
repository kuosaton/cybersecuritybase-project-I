from django.db.models import F
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


def indexView(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by(
        "-pub_date"
    )[:5]
    context = {"questions": questions}
    return render(request, "polls/index.html", context)


def registerView(request):
    if request.method == "GET":
        return render(request, "polls/register.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        if password != password_confirmation:
            return render(
                request,
                "polls/register.html",
                {
                    "error_message": "Passwords do not match",
                },
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "polls/register.html",
                {"error_message": "Username already exists"},
            )

        User.objects.create_user(username=username, password=password)
        return redirect("polls:index")


# Uncomment to correctly prevent users from accessing login only page
# This fixes A01:2021-Broken Access Control for addView
# @login_required(redirect_field_name="")
@csrf_exempt  # Remove this decorator to restore CSRF protection
def deleteView(request, pk):
    question = Question.objects.get(pk=pk)

    """
    # Remove quotation comment marks to prevent users from deleting other users' questions
    # This fixes A01:2021
    if question.creator != request.user:
        return redirect("/")
    """
    question.delete()
    return redirect("/")


# Uncomment to correctly prevent users from accessing login only page
# This fixes A01:2021-Broken Access Control for addView
# @login_required(redirect_field_name="")
@csrf_exempt  # Remove this decorator to restore CSRF protection
def addView(request):
    if request.method == "POST":
        question_text = request.POST.get("question_text")

        choices = [
            request.POST.get("choice1_text"),
            request.POST.get("choice2_text"),
            request.POST.get("choice3_text"),
        ]

        user = request.user
        time = timezone.now()
        question = Question.objects.create(
            question_text=question_text, pub_date=time, creator=user
        )

        for choice_text in choices:
            Choice.objects.create(question=question, choice_text=choice_text)

        return redirect("polls:index")


# Uncomment to correctly prevent users from accessing login only page
# This fixes A01:2021-Broken Access Control for addView
# @login_required
@csrf_exempt  # Remove this decorator to restore CSRF protection
def detailView(request, pk):
    queryset = Question.objects.filter(pub_date__lte=timezone.now())
    question = get_object_or_404(queryset, pk=pk)
    context = {"question": question}

    return render(request, "polls/detail.html", context)


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# Uncomment to correctly prevent users from accessing login only page
# This fixes A01:2021-Broken Access Control for addView
# @login_required(redirect_field_name="")
@csrf_exempt  # Remove this decorator to restore CSRF protection
def voteView(request, pk):
    queryset = Question.objects.filter(pub_date__lte=timezone.now())

    question = get_object_or_404(queryset, pk=pk)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing with POST data
        # This prevents data from being posted twice if a user hits the Back button
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
