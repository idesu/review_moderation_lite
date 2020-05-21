import re
import string

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .forms import ReviewForm
from .models import Doctor, ExceptionWord, Fword, Review


@staff_member_required
def show_reviews(request):
    
    def word_to_check(word):
        return word.lower().translate(str.maketrans("", "", string.punctuation))

    def highlight_f_words(word, f_words, exceptions):
        if (
            word_to_check(word).startswith(f_word) or word_to_check(word).endswith(f_word)
        ) and not word_to_check(word) in exceptions:
            return word.replace(word, f'<span style="color: red;">{word}</span>')
        return word

    review_list = Review.objects.select_related("author").prefetch_related("doctor__spec").order_by(
        "dt_created"
    )
    f_words = [f.word for f in Fword.objects.all()]
    exceptions = [e.word.lower() for e in ExceptionWord.objects.all()]
    for review in review_list:
        for f_word in f_words:
            if review.formatted_text.lower().find(f_word):
                formatted_list = (
                    highlight_f_words(word, f_words, exceptions)
                    for word in review.formatted_text.split()
                )
                review.formatted_text = " ".join(formatted_list)
    paginator = Paginator(review_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator})


def new_review(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == "POST":
        instance = Review(doctor=doctor)
        if not request.user.is_anonymous:
            instance.author = request.user
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        instance.ip_address = ip
        form = ReviewForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Отзыв успешно отправлен")
        return render(request, "new_review.html", {"doctor": doctor, "form": form,})

    form = ReviewForm()
    return render(request, "new_review.html", {"doctor": doctor, "form": form,})
