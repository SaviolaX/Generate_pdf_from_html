from django.shortcuts import redirect
from django.contrib.auth import login, authenticate


def authenticate_and_login(request):
    """
    Get data from html forms,
    authenticate => login
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
    else:
        return redirect('index')

    return redirect('index')
