import json
import requests

def validate(request):
    token = request.COOKIES.get('jwt')

    if not token:
        return None, ('missing credentials', 401)
    
    url = "http://127.0.0.1:8000/api/validate/"

    response = requests.post(url=url, data={'jwt':token})

    if response.status_code == 200:
        return response.json(), None
    else:
        return None, (response, response.status_code) 