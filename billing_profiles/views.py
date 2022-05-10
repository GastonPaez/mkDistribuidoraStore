from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

class BillingProfileListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'billing_profile/billing_profiles.html'

    def get_queryset(self):
        return self.request.user.billing_profiles

@login_required(login_url='login')
def create(request):
    return render(request, 'billing_profiles/create.html', {

    })