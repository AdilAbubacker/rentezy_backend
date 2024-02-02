import json
import requests
import os

def validate(request):
    token = request.COOKIES.get('jwt')

    if not token:
        return None, ('missing credentials', 401)
    
    # url = f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/api/validate/"
    url = "http://127.0.0.1:8000/api/validate/"

    response = requests.post(url=url, data={'jwt':token})

    if response.status_code == 200:
        return response.json(), None
    else:
        return None, (response, response.status_code) 