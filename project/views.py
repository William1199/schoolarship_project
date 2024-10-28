from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from articles.models import Articles
def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Tạo user nhưng chưa lưu vào database
            if not form.cleaned_data.get('is_student'):
                # Nếu không phải là sinh viên, đặt các trường bổ sung về None
                user.gpa = None
                user.language_score = None
                user.language_certificate = None
                user.desired_study_country = None
                user.degree_interest = None
            user.save()  # Lưu vào database
            messages.success(request, "Account created successfully")
            return redirect("index")

    context = {"form": form}
    return render(request, 'project/signup.html', context)

def signin(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.warning(request, "Wrong email or password! Please try again")
            return redirect("signin")

    context = {}
    return render(request, 'project/login.html', context)

def signout(request):
    logout(request)
    return redirect("index")


def profile(request):
    context = {}
    return render(request, "project/profile.html", context)

# @login_required(login_url="signin")
# def profile(request):
#     user = request.user
#     articles = Articles.objects.filter(user=user)
#     context = {"user": user, "articles": articles}
#     return render(request, "project/profile.html", context)


# @login_required(login_url="signin")
# def update_profile(request):
#     if request.user.is_authenticated:
#         user = request.user
#         form = UpdateProfileForm(instance=user)
#         if request.method == 'POST':
#             form = UpdateProfileForm(request.POST, request.FILES, instance=user)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Profile updated successfully")
#                 return redirect("profile")
#
#     context = {"form": form}
#     return render(request, "core/update_profile.html", context)