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
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


def indexView(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by(
        "-pub_date"
    )[:5]
    context = {"questions": questions}
    return render(request, "polls/index.html", context)


"""
The 'registerView()' function suffers from 1 flaw

FLAW #1: A07:2021-Identification and Authentication Failures
    - Users are able to create an user with a weak or common password
    - The flaw can be fixed by uncommenting 'validate_password()'
    - This adds weak password checks for registration
"""


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
        try:
            # Uncomment 'validate_password()' to add weak password checks
            # validate_password(password=password)
            User.objects.create_user(username=username, password=password)

            return render(
                request,
                "polls/register.html",
                {"success_message": f"Account {username} created successfully!"},
            )

        except ValidationError as e:
            return render(
                request,
                "polls/register.html",
                {"error_message": e},
            )


"""
The 'deleteView()' function suffers from 2 flaws

FLAW #1: A01:2021-Broken Access Control
    - Users are able to delete other users' polls; they don't even have to be logged in
    - This is not intended; users should be logged in and only be able to delete their own polls
    - The flaw can be fixed by:
        - 1. Uncommenting '@login_required'
        - 2. removing the quotation commenting around the 'question.creator != request.user check'
FLAW #2: CSRF vulnerability
    - The function is missing CSRF protection
    - The flaw can be fixed by removing the '@csrf_exempt' decorator
"""


# @login_required(redirect_field_name="") # Uncomment this decotator
@csrf_exempt  # Remove this decorator
def deleteView(request, pk):
    question = Question.objects.get(pk=pk)

    # Remove quotation commenting around this if-statement
    """
    if question.creator != request.user:
        return redirect("/")
    """
    question.delete()
    return redirect("/")


"""
The 'detailview()' function suffers from 2 flaws

FLAW #1: A01:2021-Broken Access Control
    - Users are able to view poll details by force browsing to their URLs
    - This functionality is meant to be login only
    - The flaw can be fixed by uncommenting '@login_required'
FLAW #2: CSRF vulnerability
    - The function is missing CSRF protection
    - The flaw can be fixed by removing the '@csrf_exempt' decorator
"""


# @login_required(redirect_field_name="") # Uncomment this decorator
@csrf_exempt  # Remove this decorator
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


"""
The 'detailview()' function suffers from 2 flaws

FLAW #1: A01:2021-Broken Access Control
    - Users are able to view poll details by force browsing to their URLs
    - This functionality is meant to be login only
    - The flaw can be fixed by uncommenting '@login_required'
FLAW #2: CSRF vulnerability
    - The function is missing CSRF protection
    - The flaw can be fixed by removing the '@csrf_exempt' decorator
"""


# @login_required # Uncomment this decorator
@csrf_exempt  # Remove this decorator
def detailView(request, pk):
    queryset = Question.objects.filter(pub_date__lte=timezone.now())
    question = get_object_or_404(queryset, pk=pk)
    context = {"question": question}

    return render(request, "polls/detail.html", context)


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


"""
The 'voteView()' function suffers from 2 flaws

FLAW #1: A01:2021-Broken Access Control
    - Users are able to vote on polls by force browsing to their URLs
    - This functionality is meant to be login only
    - The flaw can be fixed by uncommenting '@login_required'
FLAW #2: CSRF vulnerability
    - The function is missing CSRF protection
    - The flaw can be fixed by removing the '@csrf_exempt' decorator
"""


# @login_required(redirect_field_name="") # Uncomment this decorator
@csrf_exempt  # Remove this decorator
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
