from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from posts.models import Post

from authors.forms import AuthorPostForm, LoginForm, RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(
        request=request, template_name='authors/pages/register_view.html',
        context={
            'form': form,
        }
    )


def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(
            request=request, message='Account registered successfully.'
        )
        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    messages.error(request, 'Error, please fix.')
    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(
        request=request, template_name='authors/pages/login.html', context={
            'form': form,
            'redirect': reverse('authors:login_create')
        })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        is_authenticated = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if is_authenticated is not None:
            messages.success(
                request=request,
                message='Login successfully.'
            )
            login(request, is_authenticated)
        else:
            messages.error(
                request=request,
                message='Invalid credentials.'
            )
    else:
        messages.error(
            request=request,
            message='Error to validate form data.'
        )
    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request=request, message='Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request=request, message='Invalid user to logout')
        return redirect(reverse('authors:login'))

    logout(request)
    messages.success(request=request, message='Logout with sucess')
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    posts = Post.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(
        request=request,
        template_name='authors/pages/dashboard.html',
        context={
            'posts': posts,
        }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_new_post(request):
    form = AuthorPostForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        post: Post = form.save(commit=False)

        post.author = request.user
        post.content_is_html = False
        post.is_published = False
        post.save()
        messages.success(request, 'Post saved successfully.')
        return redirect(
            reverse('authors:dashboard_post_edit', args=(post.pk,)))

    return render(
        request=request,
        template_name='authors/pages/dashboard_new_post.html',
        context={
            'form': form,
            'form_action': reverse('authors:dashboard_new_post')
        }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_post_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    post = Post.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()

    if not post:
        raise Http404()

    post.delete()
    messages.success(request, 'Deleted succesfully')
    return redirect(reverse('authors:dashboard'))
