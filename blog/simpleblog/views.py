from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'simpleblog/post/list.html'

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 2)  # 5 постов на каждой странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не целое число, то отправляем первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница вне диапазона, то отправляет последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request, 'simpleblog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'simpleblog/post/detail.html', {'post': post})
