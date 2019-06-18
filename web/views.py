from django.http.response import JsonResponse
from django.views.generic import View

from web.models import DemoUser


def api_common(data={}, code=0, message='lang.success'):
    response = {
        'data': data,
        'return_code': code,
        'return_message': message
    }
    return response


class APIUserSearchView(View):
    def post(self, request):
        username = request.POST.get('username', '')
        userlist = []
        if username:
            ggac_users = DemoUser.objects.filter(username__icontains=username)
            for ggac_user in ggac_users:
                userlist.append({
                    'id': ggac_user.id,
                    'username': ggac_user.username,
                })
            data = {
                'userlist': userlist
            }
        else:
            data = {
                'userlist': []
            }
        response = api_common(data, 0, 'success')
        response_json = JsonResponse(response)
        return response_json
