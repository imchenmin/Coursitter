from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.


def login_view(request):
    if request.method == 'GET':
        return render(request,'user_login.html')

    else:
        username = request.POST['username']
        password = request.POST['password']
        print('logininginging')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')

            ...
        else:
            # Return an 'invalid login' error message.
            ...


def logout_view(request):
    logout(request)
    return render(request,"user_login.html")
    # Redirect to a success page.


@login_required(login_url='/login')
def userMain(request):
    return render(request, "user_main.html")