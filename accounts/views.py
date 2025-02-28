from django.shortcuts import render
from .forms import UserCreationForm
from django.views import View




class UserRegistrationView(View):
    form_class = UserCreationForm
    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form':form})
    
    def post(self, request):
        pass