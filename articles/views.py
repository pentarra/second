from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Article
from .forms import ArticleForm
from django.utils import timezone

def index(request):
	latest_articles_list = Article.objects.order_by('-pub_date')[:5]
	return render(request, 'articles/list.html', {'latest_articles_list': latest_articles_list})

def detail(request, article_id):
	try:
		a = Article.objects.get( id =  article_id )
	except:
		raise Http404('Статья не найдена')
	latest_comments_list = a.comment_set.order_by('-id')[:10]
	return render(request, 'articles/detail.html', {'article': a, 'latest_comments_list': latest_comments_list})

def leave_comment(request, article_id):
	try:
		a = Article.objects.get( id =  article_id)
	except:
		raise Http404('Статья не найдена')
	a.comment_set.create(author_name = request.POST['name'], comment_text = request.POST['text'])
	return HttpResponseRedirect(reverse('articles:detail', args  = (a.id, )))

def post_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('detail', article_id=post.id)
    else:
        form = ArticleForm()
    return render(request, 'articles/post_edit.html', {'form': form})

def post_edit(request, article_id):
    post = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('articles:detail', article_id=post.id)
    else:
        form = ArticleForm(instance=post)
    return render(request, 'articles/post_edit.html', {'form': form})

