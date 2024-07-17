from django.shortcuts import render

# Create your views here.
def blocked(request):
    return render(request, 'blocked.html')