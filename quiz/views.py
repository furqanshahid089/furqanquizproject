from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Category, Subcategory, Question, QuizResult, QuizAnswer


def home(request):
    categories = Category.objects.all()

    return render(request, 'quiz/home.html', {
        'categories': categories
    })


@login_required
def quiz(request, id):
    category = get_object_or_404(Category, id=id)
    subcategories = category.subcategories.all()

    if subcategories.exists():
        return render(request, 'quiz/subcategories.html', {
            'category': category,
            'subcategories': subcategories,
        })

    return take_quiz(request, category)


@login_required
def subcategory_quiz(request, id, subcategory_id):
    category = get_object_or_404(Category, id=id)
    subcategory = get_object_or_404(
        Subcategory,
        id=subcategory_id,
        category=category
    )
    return take_quiz(request, category, subcategory)


def take_quiz(request, category, subcategory=None):
    questions = Question.objects.filter(category=category)
    if subcategory:
        questions = questions.filter(subcategory=subcategory)

    total_questions = questions.count()

    if total_questions == 0:
        return render(request, 'quiz/quiz.html', {
            'category': category,
            'subcategory': subcategory,
            'questions': questions,
            'no_questions': True
        })

    if request.method == "POST":
        score = 0
        submitted_answers = []

        for question in questions:
            selected_answer = request.POST.get(
                f"question{question.id}"
            ) or ""

            is_correct = selected_answer == question.answer

            if is_correct:
                score += 1

            submitted_answers.append({
                'question': question,
                'selected_answer': selected_answer,
                'is_correct': is_correct
            })

        percentage = round((score / total_questions) * 100, 2)

        result = QuizResult.objects.create(
            user=request.user,
            category=category,
            subcategory=subcategory,
            score=score,
            total_questions=total_questions,
            percentage=percentage
        )

        for answer_data in submitted_answers:
            QuizAnswer.objects.create(
                result=result,
                question=answer_data['question'],
                selected_answer=answer_data['selected_answer'],
                is_correct=answer_data['is_correct']
            )

        return render(request, 'quiz/result.html', {
            'result': result,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'category': category,
            'subcategory': subcategory
        })

    return render(request, 'quiz/quiz.html', {
        'category': category,
        'subcategory': subcategory,
        'questions': questions
    })


@login_required
def my_results(request):
    results = QuizResult.objects.filter(
        user=request.user
    ).order_by('-completed_at')

    return render(request, 'quiz/my_results.html', {
        'results': results
    })


def leaderboard(request):
    results = QuizResult.objects.order_by(
        '-percentage',
        '-score',
        'completed_at'
    )[:10]

    return render(request, 'quiz/leaderboard.html', {
        'results': results
    })


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {
        'form': form
    })
