from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from users.models import User

from django.contrib import messages

from products.models import Product
from .forms import RegisterForm
from products.models import Product

def index(request):
    products = Product.objects.all().order_by('-id')

    return render(request, 'index.html', {
        'message': ' Lista de productos',
        'title': 'Productos',
        'products': products,
    
    })


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
                        
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])

            return redirect('index')
        else:
            messages.error(request, 'Usuario o Contraseña no valido')
    return render(request, 'users/login.html',
                  {

                  })


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)
    # Si la peticion es POST genera un formulario con los datos enviados, sino con campos vacios.
    if request.method == 'POST' and form.is_valid():
        """
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = User.objects.create_user(username, email, password)
        """
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, 'Usuario Creado exitosamente')
            return redirect('index')

    return render(request, 'users/register.html', {
        'form': form
    })
