from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from .forms import SignUp
from .models import User
from django.db import transaction
from django.contrib.auth import login
from django.views.generic import View, ListView, UpdateView, DeleteView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class UserView(View):
    @transaction.atomic
    def get(self, request):
        form = SignUp
        return render(request, 'signup.html', {'form': form})

    @transaction.atomic
    def post(self, request):
        form = SignUp(request.POST)
        if form.is_valid():
            user = form.save(request)
            user.verification = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Verify your Project Allocation account.'
            message = render_to_string('verify_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('userdashboard')
        return render(request, "signup.html", {'form': form, 'error': 'error'})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.verification = True
        user.save()
        message = 'Thank you for your email confirmation. Now you can login your account.'
        return render(request, 'base.html', {'message': message})
    else:
        return HttpResponse('Activation link is invalid!')


class UserList(View):

    def get(self, request):
        user_list_list = User.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(user_list_list, 5)
        try:
            user_list = paginator.page(page)
        except PageNotAnInteger:
            user_list = paginator.page(1)
        except EmptyPage:
            user_list = paginator.page(paginator.num_pages)
        return render(request, 'employeelist.html', {'user_list': user_list})


class UserUpdateView(UpdateView):
    template_name = 'registration/update.html'
    model = User
    success_url = 'dashboard'
    fields = ['name', 'username', 'phone', 'email', 'percentage']
    context_object_name = 'form'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(User, id=id)

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        return redirect("employeelist")


class UserDeleteView(DeleteView):
    model = User
    context_object_name = 'form'
    success_url = reverse_lazy('employeelist')
    template_name = 'registration/delete.html'


class EmployeeSearchView(View):

    def get(self, request):
        q = request.GET.get('q', None)
        try:
            int(q)
            user_list_list = User.objects.filter(Q(percentage=int(q)) | Q(name__icontains=q) | Q(username__icontains=q) | Q(email__icontains=q))
        except ValueError:
            user_list_list = User.objects.filter(
                Q(name__icontains=q) | Q(username__icontains=q) | Q(email__icontains=q))
        if user_list_list:
            page = request.GET.get('page', 1)
            paginator = Paginator(user_list_list, 5)
            try:
                user_list = paginator.page(page)
            except PageNotAnInteger:
                user_list = paginator.page(1)
            except EmptyPage:
                user_list = paginator.page(paginator.num_pages)
            return render(request, 'employeelist.html', {'user_list': user_list, 'q': q})
        else:
            error = "No such data found."
            user_list_list = User.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(user_list_list, 5)
            try:
                user_list = paginator.page(page)
            except PageNotAnInteger:
                user_list = paginator.page(1)
            except EmptyPage:
                user_list = paginator.page(paginator.num_pages)
            return render(request, 'employeelist.html', {'user_list': user_list, 'error': error})