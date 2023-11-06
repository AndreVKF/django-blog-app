from django.http import HttpResponse

def checkUserNotAllowedIntoRoom(request, room):
    if request.user != room.host:
        return HttpResponse('Not allowed', status=401)