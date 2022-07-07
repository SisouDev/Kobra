from authors.forms import AuthorPostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from posts.models import Post


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardPost(View):
    def get_post(self, id=None):
        post = None

        if id is not None:
            post = Post.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not post:
                raise Http404()
        return post

    def get(self, request, id=None):
        post = self.get_post(id)
        form = AuthorPostForm(instance=post)

        if id is None:
            return render(
                request=self.request,
                template_name='authors/pages/dashboard_new_post.html',
                context={
                    'form': form,
                    'form_action': reverse('authors:dashboard_new_post')
                }
            )

        return render(
            request=self.request,
            template_name='authors/pages/dashboard_post.html',
            context={
                'form': form,
            }
        )

    def post(self, request, id=None):
        post = self.get_post(id)

        form = AuthorPostForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=post
        )

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.content_is_html = False
            post.is_published = False

            post.save()
            messages.success(request, 'Post saved successfully.')
            return redirect(reverse('authors:dashboard_post_edit', args=(
                post.pk,
            )))

        return render(
            request=self.request,
            template_name='authors/pages/dashboard_new_post.html',
            context={
                'form': form,
                'form_action': reverse('authors:dashboard_new_post')
            }
        )
