from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView

from core.forms import UserProfileForm
from core.models import UserProfile, Site, TrafficStatistics


class BaseView(TemplateView):
    template_name = "base.html"


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('core:user_profile')


class UserProfileView(LoginRequiredMixin, TemplateView, FormView):
    template_name = "user_profile.html"
    form_class = UserProfileForm
    success_url = "core:user_profile"

    def get(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        form_data = request.session.get("profile")
        if form_data:
            form = self.form_class(initial=form_data)
        else:
            form = self.form_class()

        return render(request, "user_profile.html", {"form": form, "user_profile": user_profile})

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]

        self.request.session["profile"] = {
            "name": name,
            "email": email
        }

        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        profile.name = name
        profile.email = email
        profile.save()

        return redirect(self.success_url)


@login_required
def proxy_view(request, user_site_name, routes_on_original_site):
    try:
        user_profile = UserProfile.objects.get(user=request.user)

        site = Site.objects.get(user_profile=user_profile, name=user_site_name)

        response = requests.get(routes_on_original_site)

        data_sent = len(request.body) if request.body else 0
        data_received = len(response.content)

        traffic_stat, created = TrafficStatistics.objects.get_or_create(user_profile=user_profile, site=site)
        traffic_stat.page_views += 1
        traffic_stat.data_sent += data_sent
        traffic_stat.data_received += data_received
        traffic_stat.save()

        soup = BeautifulSoup(response.text, 'html.parser')
        base_url_with_site_name = f"http://localhost/{user_site_name}/"

        for tag in soup.find_all(['a', 'link', 'script'], href=True):
            tag['href'] = urljoin(base_url_with_site_name, tag['href'])

        for tag in soup.find_all(['img', 'script'], src=True):
            tag['src'] = urljoin(base_url_with_site_name, tag['src'])

        modified_content = str(soup)
        # context = {'modified_content': modified_content, "site": site}
        # return render(request, 'vpn.html', context, content_type=response.headers['Content-Type'])
        return HttpResponse(modified_content, content_type=response.headers['Content-Type'])

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error: {e}", status=500)


class SiteCreateView(LoginRequiredMixin, CreateView):
    model = Site
    template_name = 'create_site.html'
    fields = ['name', 'url']
    success_url = reverse_lazy('core:user_profile')

    def form_valid(self, form):
        user_profile = UserProfile.objects.get(user=self.request.user)
        form.instance.user_profile = user_profile
        return super().form_valid(form)
