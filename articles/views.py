from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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
    context = {"form": form}
    return render(request, "articles_template/create.html", context)