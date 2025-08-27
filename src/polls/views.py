from django.db.models import F
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from .models import Choice, Question
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import logging

logger = logging.getLogger(__name__)


def indexView(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by(
        "-pub_date"
    )[:5]
    context = {"questions": questions}
    return render(request, "polls/index.html", context)


# ! Flaw 1: A01:2021 - Broken Access Control
# ! Problem: Users can delete polls made by others by force browsing to a poll's deletion url (e.g. /1/delete)
# ! Fix: Uncomment the "if question.creator != request.user" checking code block
@login_required(redirect_field_name="")
def deleteView(request, pk):
    question = Question.objects.get(pk=pk)

    # ! Uncomment the below code to fix flaw A01:2021
    """
    if question.creator != request.user:
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Only the poll creator can delete it",
            },
        )
    """

    question.delete()
    return redirect("/")


@login_required(redirect_field_name="")
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

        return redirect("/")


@login_required()
def detailView(request, pk):
    queryset = Question.objects.filter(pub_date__lte=timezone.now())
    question = get_object_or_404(queryset, pk=pk)
    context = {"question": question}

    return render(request, "polls/detail.html", context)


# ! Flaw 5: CSRF vulnerability
# ! Problem: voteView() is missing CSRF protection
# ! Fix: Remove the @csrf_exempt decorator
@csrf_exempt  # ! Remove this to fix CSRF flaw
@login_required(redirect_field_name="")
def voteView(request, pk):
    queryset = Question.objects.filter(pub_date__lte=timezone.now())

    question = get_object_or_404(queryset, pk=pk)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
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

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


@login_required
def resultsView(request, pk):
    queryset = Question.objects.filter(pub_date__lte=timezone.now())
    question = get_object_or_404(queryset, pk=pk)
    context = {"question": question}

    return render(request, "polls/results.html", context)


# ! Flaw 3: A07:2021 - Identification and Authentication Failures
# ! Problem: Users are allowed to register using a weak/common password
# ! Fix: Uncomment the validate_password() function call
# ! Note: The checks are defined in config/settings.py with the AUTH_PASSWORD_VALIDATORS dict
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
            # validate_password(password=password) # ! Uncomment this to fix flaw A07:2021
            User.objects.create_user(username=username, password=password)

            return render(
                request,
                "polls/register.html",
                {"success_message": f"Account '{username}' created successfully!"},
            )

        except ValidationError as e:
            return render(
                request,
                "polls/register.html",
                {"error_message": e},
            )
