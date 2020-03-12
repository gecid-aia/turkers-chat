from django.http import HttpResponseRedirect


def redirect_if_exchanges_with_turkers_middleware(get_response):

    def middleware(request):
        if "withturkers.net" in request.get_host():
            return HttpResponseRedirect('http://turkers.aarea.co/')

        response = get_response(request)
        return response

    return middleware
