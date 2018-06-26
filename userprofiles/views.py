from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import (
    render, 
    get_object_or_404, 
    redirect
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
#models
from persons.models import Person

@login_required()
def auth_home(request):
	return redirect('/home/')

@login_required()
def auth_dashboard(request):
	person_count = Person.objects.count()
	context = {
		'person_count': person_count
	}
	return render(request, 'dashboard.html', context)

def auth_copresa(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:		
		if request.method == 'POST':
			action = request.POST.get('action', None)
			username = request.POST.get('username', None)
			password = request.POST.get('password', None)

			if action == 'signup':
				pass
			elif action == 'login':
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						if 'next' in request.GET:
							return HttpResponseRedirect(request.GET['next'])
						else:
							return HttpResponseRedirect('/')
					else:
						messages.add_message(request, messages.ERROR, 'Su cuenta ha sido desactivado.')
						return render(request, 'auth/signin.html')
				else:
					messages.add_message(request, messages.ERROR, 'Usuario y/o contraseña incorrectos')
					return render(request, 'auth/login.html')
			
		context = {}
		return render(request, 'auth/login.html', context)