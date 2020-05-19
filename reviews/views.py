from django.contrib import messages
from django.shortcuts import get_object_or_404, render

from .forms import ReviewForm
from .models import Doctor, Review


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
        return render(request, 'Review.html', {
            'doctor': doctor,
            'specs': specs,
            'form': form, })

    form = ReviewForm()
    return render(request, 'Review.html', {'doctor': doctor, 'specs': specs, 'form': form, })
