from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q
from .forms import CreateArticleForm, CommentForm
from .models import Articles, Comment, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def index(request):
    keyword = request.GET.get("search")
    paginator = None
    msg = None

    if keyword:
        articles = Articles.objects.filter(
            Q(title__icontains=keyword) | Q(information__icontains=keyword) | Q(category__title__icontains=keyword))
        if articles.exists():
            paginator = Paginator(articles, 4)
            articles = paginator.page(1)
        else:
            msg = f'There is no article with the keyword "{keyword}"'
    else:
        articles = Articles.objects.filter(featured=False)
        paginator = Paginator(articles, 4)
        page = request.GET.get("page")

        try:
            articles = paginator.page(page)

        except PageNotAnInteger:
            articles = paginator.page(1)

        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    # featured_articles = Articles.objects.get(featured=True) "f_articles": featured_articles
    context = {"articles": articles, "msg": msg, "paginator": paginator, "cats": categories}
    return render(request, "articles_template/index.html", context)


def detail(request, slug):
    keyword = request.GET.get("search")
    msg = None

    if keyword:
        article = Articles.objects.filter(
            Q(title__icontains=keyword) | Q(information__icontains=keyword) | Q(category__title__icontains=keyword))
        if article.exists():
            pass
        else:
            msg = f'There is no article with the keyword "{keyword}"'

    article = Articles.objects.get(slug=slug)
    related_articles = Articles.objects.filter(category__id=article.category.id).exclude(id=article.id)[:4]
    comments = Comment.objects.filter(article=article)
    form = CommentForm()
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.user = request.user
                comment.save()
                messages.success(request, "Your comment has been posted.")
                return redirect("detail", slug=article.slug)
    context = {"articles": article, "form": form, "comments": comments, "r_articles": related_articles, "msg": msg}
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


@login_required(login_url="signin")
def update_article(request, slug):
    update = True
    article = Articles.object.get(slug=slug)
    form = CreateArticleForm(instance=article)
    if request.method == "POST":
        form = CreateArticleForm(request.POST, request.FILES, instance=article)
        article = form.save(commit=False)
        article.slug = slugify(request.POST["title"])
        article.save()
        messages.success(request, "Articles updated successfully!")
        return redirect("profile")
    context = {"update": update}
    return render(request, "articles_template/create.html", context)


@login_required(login_url="signin")
def delete_article(request, slug):
    # article = Articles.objects.get(slug=slug)
    article = get_object_or_404(Articles, slug=slug)
    articles = Articles.objects.filter(user=request.user)
    delete_article = True
    if request.method == "POST":
        article.delete()
        messages.success(request, "Deleted successfully!")
        return redirect("profile")
    context = {"article": article, "del": delete_article, "articles": articles}
    return render(request, "project/profile.html", context)
