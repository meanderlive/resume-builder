from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView,  UpdateView, DetailView
from portfolio.forms import UserForm, PortfolioForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from portfolio.models import Portfolio
from django.contrib.auth.mixins import LoginRequiredMixin


 
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# Create your views here.
class Home(TemplateView):
    template_name = 'portfolio/index.html'

class personal_info(LoginRequiredMixin, CreateView):
    login_url = '/signin/'
    form_class = PortfolioForm
    model = Portfolio
    context_name = "form"
    template_name = 'portfolio/personal_info.html'
    print( "The task was created successfully.")
 

    def form_valid(self, form):
        obj = form.save(commit=False)
        print(obj)
        obj.username = self.request.user
        obj.save()
      
        return  redirect('cv_template')
  

class UpdatePersonal_info(LoginRequiredMixin, UpdateView):
    login_url = '/signin/'
    form_class = PortfolioForm
    model = Portfolio
    context_name = "form"
    template_name = 'portfolio/personal_info.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.username = self.request.user
        obj.save()
        return redirect('cv_template')

class cv_list(ListView):
    template_name = 'portfolio/cv_list.html'
    model = Portfolio
    context_object_name = 'port'

class test_template(LoginRequiredMixin, ListView):
    login_url = '/signin/'
    model= Portfolio
    template_name = 'portfolio/templates/index_1.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('context',context)
        context['ports'] = Portfolio.objects.get(username__username=self.request.user.username)
        return context

class text_template2(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    model = Portfolio
    template_name = 'portfolio/templates/index_2.html'
    def get_context_data(self, **kwargs):
        print('kwargs',kwargs)
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username = self.request.user.username)
        return context

class text_template3(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    template_name = 'portfolio/templates/index_3.html'
    model = Portfolio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['ports'] = Portfolio.objects.get(username__username = self.request.user.username)
        return context  

class text_template4(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    model = Portfolio
    template_name = 'portfolio/templates/index_4.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username=self.request.user.username)
        return context

class text_template5(LoginRequiredMixin, TemplateView):
    login_url = '/signin/'
    template_name = "portfolio/templates/index_5.html"
    model = Portfolio
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ports'] = Portfolio.objects.get(username__username = self.request.user.username)
        return context
           

###############################      REGISTER    #################################
def signup_user(request):
    form_name = UserForm()
    if request.method =="POST":
        form_name = UserForm(request.POST)
        if form_name.is_valid():
            form_name.save()
            messages.success(request, "You have registered successfully")
            return redirect('signin')
        else:
            messages.error(request, 'Invalid input') 
            return redirect('signup')
    else:
        context = {'form_name':form_name}
        return render(request, 'portfolio/signup.html', context)

def signin_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cv_template')
        else:
            messages.info(request, 'Invalid input.. Please try again.')
            return redirect('signin')
    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'portfolio/signin.html', context)

# def password_reset_request(request):
#     if request.method == "POST":
#         domain = request.headers['Host']
#         password_reset_form = PasswordResetForm(request.POST)
#         if password_reset_form.is_valid():
#             data = password_reset_form.cleaned_data['email']
#             associated_users = User.objects.filter(Q(email=data))
#             # You can use more than one way like this for resetting the password.
#             # ...filter(Q(email=data) | Q(username=data))
#             # but with this you may need to change the password_reset form as well.
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Password Reset Requested"
#                     email_template_name = "portfolio/password_reset_email.txt"
#                     c = {
#                         "email": user.email,
#                         'domain': domain,
#                         'site_name': 'Interface',
#                         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                         "user": user,
#                         'token': default_token_generator.make_token(user),
#                         'protocol': 'http',
#                     }
#                     email = render_to_string(email_template_name, c)
#                     try:
#                         send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
#                     except BadHeaderError:
#                         return HttpResponse('Invalid header found.')
#                     return redirect("/portfolio/password_reset/done/")
#     password_reset_form = PasswordResetForm()
#     return render(request=request, template_name="portfolio/password_reset.html",
#                   context={"password_reset_form": password_reset_form})

def logout_user(request):
    logout(request)
    return redirect('signin')
    
        

# for testing
def index(request):
    return render(request, "portfolio/index.html")