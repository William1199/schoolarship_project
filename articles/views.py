from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q
from .forms import CreateArticleForm
from .models import Articles

# Create your views here.
def index(request):
    featured_articles = Articles.objects.get(featured=True)
    articles = Articles.objects.filter(featured=False)
    context = {"articles": articles, "f_articles": featured_articles}
    return render(request, "articles_template/index.html", context)

def detail(request, slug):
    articles = Articles.objects.get(slug=slug)
    context = {"articles": articles}
    return render(request, "articles_template/detail.html", context)

@login_required(login_url="signin")
def create_article(request):
    form = CreateArticleForm()
    if request.method == "POST":
        form = CreateArticleForm(request.POST, request.FILES)
        if form.is_valid():
            articles = form.save(commit=False)
            articles.slug = slugify(request.POST["title"])
            articles.user = request.user
            articles.username = request.user.username
            articles.save()
            messages.success(request, "Articles created successfully!")
            return redirect("profile")
    context = {"form": form}
    return render(request, "articles_template/create.html", context)

def update_article(request,slug):
    update = True
    article = Articles.object.get(slug=slug)
    form = CreateArticleForm(instance=article)
    if request.method == "POST":
        article = form.save(commit=False)
        article.slug = slugify(request.POST["title"])
        article.save()
        messages.success(request, "Articles updated successfully!")
        return redirect("profile")
    context = {"update": update}
    return render(request, "articles_template/create.html", context)