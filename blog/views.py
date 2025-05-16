from ast import Mult
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .models import Blog, Comment
from .forms import CommentForm, ContactForm
from .models import Product, Service
from .models import Technology




def home(request):
    posts = Blog.objects.filter(status=1).order_by('-published_date')
    read_more_posts = Blog.objects.filter(status=1).order_by('-published_date')[3:6]
    recent_posts = Blog.objects.filter(status=1).order_by('-published_date')[:5]
    categories = Blog.objects.values_list('category', flat=True).distinct()

    return render(request, 'blog_home.html', {
        'posts': posts,
        'read_more_posts': read_more_posts,
        'recent_posts': recent_posts,
        'categories': categories,
    })


def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    comments = post.comments.filter(parent__isnull=True).order_by('-date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post

            parent_id = request.POST.get('parent_id')
            if parent_id:
                new_comment.parent = Comment.objects.get(id=parent_id)

            new_comment.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = CommentForm()

    related_posts = Blog.objects.filter(category=post.category).exclude(pk=post.pk)[:3]

    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog_detail.html', {
        'post': post,
        'comments': page_obj.object_list,
        'page_obj': page_obj,
        'form': form,
        'related_posts': related_posts,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"New Contact Message from {name}"
            message_body = f"""
                <html>
                    <body>
                        <h2>Contact Message</h2>
                        <p><strong>Name:</strong> {name}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Message:</strong> {message}</p>
                    </body>
                </html>
            """

            send_mail(
                subject,
                message_body,
                email,
                [settings.CONTACT_EMAIL],
                html_message=message_body,
            )
            return render(request, 'contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def blog(request):
    category = request.GET.get('category')
    if category:
        posts = Blog.objects.filter(status=1, category=category).order_by('-published_date')
    else:
        posts = Blog.objects.filter(status=1).order_by('-published_date')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Blog.objects.values_list('category', flat=True).distinct()

    return render(request, 'blog.html', {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'categories': categories,
        'selected_category': category,
    })


def posts_by_category(request, category):
    posts = Blog.objects.filter(status=1, category=category).order_by('-published_date')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Blog.objects.values_list('category', flat=True).distinct()

    return render(request, 'blog.html', {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category,
    })


def about(request):
     return render(request, 'about.html')

def products_view(request):
    products = Product.objects.all()
    return render(request, 'blog/products.html', {'products': products})

def services_view(request):
    services = Service.objects.all()
    return render(request, 'blog/services.html', {'services': services})


def multi_tch_view(request):
    technologies = Technology.objects.all()
    return render(request, 'multi-tch.html', {'technologies': technologies})

