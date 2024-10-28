from django.shortcuts import render
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