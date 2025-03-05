import requests
from django.http import JsonResponse

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            # Validate token with the customer service
            response = requests.post('http://customer:8001/api/validate_token/', data={'token': token_key})
            if response.status_code == 200:
                user_id = response.json()['user_id']
                request.META['HTTP_X_USER_ID'] = str(user_id)
            else:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        response = self.get_response(request)
        return response