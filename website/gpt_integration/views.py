
from django.http import JsonResponse
from .utils import generate_text

def generate_response(request):
    prompt = request.POST.get('prompt')
    if prompt:
        response = generate_text(prompt)
        return JsonResponse(response, safe=False)
    else:
        return JsonResponse({'error': 'No prompt provided'}, status=400)
