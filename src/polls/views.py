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


def indexView(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by(
        "-pub_date"
    )[:5]
    context = {"questions": questions}
    return render(request, "polls/index.html", context)


@login_required(redirect_field_name="")
def deleteView(request, pk):
    question = Question.objects.get(pk=pk)

    # // Flaw 1 (A01:2021) fix: Uncomment the below code //
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


# // Flaw 5 (CSRF) fix: Remove @csrf_exempt //
@csrf_exempt
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


def registerView(request):
    if request.method == "GET":
        return render(request, "polls/register.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "polls/register.html",
                {"error_message": "Username already exists"},
            )

        if password != password_confirmation:
            return render(
                request,
                "polls/register.html",
                {
                    "error_message": "Passwords do not match",
                    "previous_username_input": username,
                },
            )

        try:
            # // Flaw 3 (A07:2021) fix: Uncomment validate_password() //
            # validate_password(password=password)
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
                {"validation_error_message": e, "previous_username_input": username},
            )
