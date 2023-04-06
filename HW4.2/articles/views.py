from django.shortcuts import render
from articles.models import Article


def articles_list(request):
    sort = request.GET.get('sort')
    if sort == 'date':
        articles = Article.objects.order_by('-published_at')
    elif sort == 'title':
        articles = Article.objects.order_by('title')
    else:
        articles = Article.objects.all()
    template = 'articles/news.html'
    context = {'articles': articles}
    return render(request, template, context)