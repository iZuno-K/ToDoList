from django.http import JsonResponse
from django.views.generic import View


class AccountsApi(View):
    def get(self, request):
        """
        return login information if certificated
        :param request:
        :return:
        """
        account = request.user
        if account.is_authenticated:
            return JsonResponse({
                'account_info': {
                    'account_id': account.id,
                    'name': account.username,
                }
            })