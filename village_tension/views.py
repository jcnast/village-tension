from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# import dad's soundcloud
def soundcloud(request):
	return render(request, 'soundcloud.html')