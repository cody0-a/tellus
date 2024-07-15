# middleware.py
from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):
        if response.status_code == 404:
            return self.handle_404(request, response)
        elif response.status_code == 500:
            return self.handle_500(request, response)
        return response

    def handle_404(self, request, response):
        context = {'message': 'The page you are looking for does not exist.'}
        return render(request, 'errors/404.html', context, status=404)

    def handle_500(self, request, response):
        context = {'message': 'An unexpected error has occurred.'}
        return render(request, 'errors/500.html', context, status=500)