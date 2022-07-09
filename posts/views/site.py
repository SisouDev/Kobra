from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from utils.categoriesname import namecat
from utils.pagination import make_pagination_range
from posts.models import Post
from tag.models import Tag


def theory(request, *args, **kwargs):
    posts = Post.objects.all()
    posts = posts.filter(title__icontains='Java')
    contexto = {
        'posts': posts,
    }
    return render(
        request=request,
        template_name='posts/theory.html',
        context=contexto
    )


class PostListViewBase(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 6
    ordering = ['-id']
    template_name = 'posts/basis.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags')
        return qs


class PostListViewHome(PostListViewBase):
    template_name: str = 'posts/basis.html'


class PostListViewSearch(PostListViewBase):
    template_name: str = 'posts/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')
        ctx.update(
            {
                'page_title': f'Search for "{search_term}"',
                'search_term': search_term,
                'additional_url_query': f'&q={search_term}',
            }
        )
        return ctx


def home(request):
    post = Post.objects.filter(
        is_published=True,
    ).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(post, 6)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    return render(
        request=request, template_name='posts/basis.html', context={
            'posts': page_obj,
            'pagination_range': pagination_range,
        }
    )


def category(request, category_id):
    name = namecat(category_id)

    if name is None:
        raise Http404('Not Found')

    post = Post.objects.filter(
        category__id=category_id, is_published=True,
    ).order_by('-id')
    return render(
        request=request, template_name='posts/category.html', context={
            'posts': post,
            'name': name,

        }
    )


def post(request, id):
    post = get_object_or_404(Post, pk=id, is_published=True,)

    return render(
        request=request, template_name='posts/post_view.html', context={
            'post': post
        }
    )


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    posts = Post.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True,
    ).order_by('-id')

    return render(request, 'posts/search.html', context={
        'page_title': f'Search for "{search_term}"',
        'search_term': search_term,
        'posts': posts,
    })


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name: str = 'posts/post_view.html'


class PostHomeListViewApi(PostListViewBase):
    template_name = 'posts/basis.html'

    def render_to_response(self, context, **response_kwargs):
        posts = self.get_context_data()['posts']
        post_values = posts.values(
            'id', 'title', 'description',
            'cover', 'category__name'
        )
        return JsonResponse(
            data=list(post_values),
            safe=False,
        )


class PostDetailViewApi(PostDetail):
    def render_to_response(self, context, **response_kwargs):
        post = self.get_context_data()['post']
        post_dict = model_to_dict(post)

        if post_dict.get('cover'):
            post_dict['cover'] = self.request.build_absolute_uri() + \
                post_dict['cover'].url[1:]
        else:
            ...

        if post_dict.get('image_post'):
            post_dict['image_post'] = self.request.build_absolute_uri() + \
                post_dict['image_post'].url[1:]
        else:
            ...

        del post_dict['is_published']

        return JsonResponse(
            data=post_dict,
            safe=False,
        )


class PostListViewTag(PostListViewBase):
    template_name: str = 'posts/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()

        if not page_title:
            page_title = 'Not Found'

        page_title = f'Posts tagged with "{page_title.name}"'

        ctx.update(
            {
                'page_title': page_title,
            }
        )
        return ctx
