import json
import urllib.request

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, render_to_response
from django.contrib import messages

from blog.forms import CommentForm
from blog.models import Post, Comment


def blog_index(request):
    """ Display blog index page which shows an overview of all
        blog posts, separated into pages with 5 posts per page.
    """
    post_list = Post.objects.all().exclude(
        archived=True).order_by("-created_on")
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    title = 'Home'
    context = {
        "title": title,
        "posts": posts
    }
    return render(request, "blog_index.html", context)


def blog_category(request, category):
    """ Display only blog posts that belong to a specific category or tag.
    """
    post_list = Post.objects.filter(
        categories__name__contains=category).exclude(
        archived=True).order_by("-created_on")
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    title = "Posts tagged " + category
    context = {
        "title": title,
        "category": category,
        "posts": posts
    }
    return render(request, "blog_category.html", context)


def blog_author(request, author):
    """ Display only blog posts that were written by a specific author.
    """
    post_list = Post.objects.filter(author__username__contains=author).exclude(
        archived=True).order_by("-created_on")
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    title = "Posts by " + author
    context = {
        "title": title,
        "author": author,
        "posts": posts
    }
    return render(request, "blog_author.html", context)


def blog_detail(request, pk):
    """ Display an individual blog post. Provides a form below the post
        for guests to leave comments. Guests must solve a reCAPTCHA before
        being allowed to submit their comment.
    """
    site_key = open('/var/www/project/recaptcha_site', 'r').read()
    secret_key = open('/var/www/project/recaptcha_secret', 'r').read()
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)

    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': secret_key,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                comment = Comment(
                    author=form.cleaned_data["author"],
                    body=form.cleaned_data["body"],
                    post=post,
                )
                comment.save()
                messages.success(request, 'Comment added successfully!')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            return redirect('blog_detail', pk)

    title = post.title
    context = {
        "title": title,
        "post": post,
        "comments": comments,
        "form": form,
        "site_key": site_key
    }
    return render(request, "blog_detail.html", context)


def about_me(request):
    """ Display the about me page which gives background about the blog owner.
    """
    post = Post.objects.get(title__exact="About Me")

    title = post.title
    context = {
        "title": title,
        "post": post,
        "about": True
    }
    return render(request, "about_me.html", context)


def handler404(request, exception, template_name="404.html"):
    """ Handles 404 or 'Page Not Found' errors.
    """
    response = render_to_response("404.html")
    response.status_code = 404
    return response


def handler500(request, template_name="500.html"):
    """ Handles 500 or 'Internal Server' errors.
    """
    response = render_to_response("500.html")
    response.status_code = 500
    return response
