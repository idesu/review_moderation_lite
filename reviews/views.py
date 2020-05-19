import re

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .forms import ReviewForm
from .models import Doctor, Fword, Review


def show_reviews(request):
    review_list = Review.objects.select_related(
        'author').order_by("dt_created")
    f_words = [f.word for f in Fword.objects.all()]
    for review in review_list:
        for word in f_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            if re.search(pattern, review.formatted_text):
                formatted_list = (
                    word.replace(word, f'<span style="color: red;">{word}</span>')
                    if re.search(pattern, word)
                    else word
                    for word in review.formatted_text.split())
                review.formatted_text = ' '.join(formatted_list)
    paginator = Paginator(review_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {'page': page, 'paginator': paginator}
    )


def new_review(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    specs = ', '.join(spec.title for spec in doctor.spec.all())
    if request.method == 'POST':
        instance = Review(doctor=doctor)
        if not request.user.is_anonymous:
            instance.author = request.user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        instance.ip_address = ip
        form = ReviewForm(
            request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв успешно отправлен')
        return render(request, 'new_review.html', {
            'doctor': doctor,
            'specs': specs,
            'form': form, })

    form = ReviewForm()
    return render(request, 'new_review.html', {'doctor': doctor, 'specs': specs, 'form': form, })
