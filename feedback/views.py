from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FeedbackForm
from .models import Feedback


class FeedbackView(View):
    template_name = 'feedback/feedback_form.html'

    def get(self, request):
        form = FeedbackForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Спасибо за ваше обращение!'
                })
            return render(request, self.template_name, {
                'form': FeedbackForm(),
                'success_message': 'Спасибо за ваше обращение!'
            })
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
        return render(request, self.template_name, {'form': form})


@csrf_exempt
def feedback_api(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Feedback submitted successfully',
                'id': feedback.id
            })
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        }, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_form.html'
    success_url = reverse_lazy('feedback:success')

    def form_valid(self, form):
        messages.success(self.request, 'Ваше обращение успешно отправлено!')
        return super().form_valid(form)


def success_view(request):
    return render(request, 'feedback/success.html')