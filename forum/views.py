from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
from django.db import IntegrityError
from accounts.models import Account
from creators.models import ForumCreators
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from .models import Forum, Post, Category

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_banned == True:
                logout(request)
                return redirect('block_template')

            return redirect('home_page')
        else:
            data = {
                'error': "Parol yoki username xato!"
            }
            return render(request, 'login.html', data)
    return render(request, 'login.html')



def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not email or not username or not password:
            data = {'error': 'Barcha maydonlarni to‘ldiring!'}
            return render(request, 'signup.html', data)
        
        try:
            user = Account.objects.create_user(username=username, email=email, password=password)
            authenticate(user)
            data = {
                'success': 'Akkauntingiz muvaffiqiyatili yaratildi!'
            }
            return render(request, 'index.html', data)

        except IntegrityError:
            data = {'error': 'Bunday foydalanuvchi allaqachon mavjud!'}
            return render(request, 'signup.html', data)
        except Exception as e:
            data = {'error': f'Xatolik yuz berdi: {str(e)}'}
            return render(request, 'signup.html', data)

    return render(request, 'signup.html')
    

@login_required
def logout_view(request):
        logout(request)
        return redirect('home_page')


# class ForumView(generic.ListView):
#     template_name = 'get_forums.html'
#     context_object_name = 'forums'
#
#     def get_queryset(self):
#         forums = get_object_or_404(Forum, forum_slug=self.kwargs['forum_slug'])
#         return forums

def ForumView(request, forum_slug):
    # print(forum_slug)
    forums = Forum.objects.filter(category__slug=forum_slug)
    get_slug = forum_slug
    user = request.user.id  # Foydalanuvchi obyektini olib olamiz
    # print(user)
    forum_creators = ForumCreators.objects.filter(
        user=user).first()  # Foydalanuvchining forum yaratuvchisi obyektini olamiz
    forum = forum_creators.forum if forum_creators else None  # Foydalanuvchining forum obyektini olamiz, agar mavjud bo'lsa
    post_last = Post.objects.filter(
        thread__forum=forum).last() if forum else None  #
    # print(forums)
    if request.method == 'POST':
        title = request.POST['title']
        file_image = request.FILES.get('image')
        category_name = request.POST['category']
        forum_about = request.POST['forum_about']
        status = request.POST['status']

        # Category obyektini topamiz yoki yangi obyekt yaratamiz
        category, created = Category.objects.get_or_create(name=category_name)

        # Forum obyektini yaratamiz
        forum = Forum.objects.create(
            category=category,
            moderator=request.user,
            forum_question=title,
            forum_image=file_image,
            forum_about=forum_about,
            status=status,
            forum_views=None,
        )
        forum.save()
        return redirect('/')

    data = {
        'forums': forums,
        'get_slug': get_slug,
        'post_last': post_last,
        'posts': Post.objects.all(),
        'forums_counter': forums.count(),
        'categorys': Category.objects.all(),
        'category_slug': forum_slug,
    }
    return render(request, 'get_forums.html', data)


@login_required
def read_and_write(request, category_slug, forum_slug):
    # Get the category
    category = get_object_or_404(Category, slug=category_slug)

    # Get the forum associated with the category
    forum = get_object_or_404(Forum, category=category, forum_slug=forum_slug)
    forum.forum_views =+ 1
    forum.save()
    # Check if the request method is POST
    if request.method == 'POST':
        # Retrieve the current user
        user = request.user
        parent_post_id = request.POST.get('parent_post_id')
        parent_post = Post.objects.filter(id=parent_post_id).first() if parent_post_id else None
        # Get the image file from the request
        file_image = request.FILES.get('image')

        # Get the forum content from the request
        forum_about = request.POST.get('forum_about')

        # Create a new post object
        post = Post.objects.create(
            forum=forum,
            thread=None,
            author=user,
            content=forum_about,
            image=file_image,
            parent_post=parent_post
        )
        # Save the post
        post.save()

        # Redirect to the success page
        return redirect(forum.post_url())

    # If the request method is not POST, retrieve posts associated with the forum
    posts = Post.objects.filter(forum=forum)
    posts_list = Post.objects.filter(forum=forum, parent_post=None).order_by('-created_at')
    paginator = Paginator(posts_list, 5)  # Show 5 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # Prepare data to pass to the template

    data = {
        'forum': forum,
        'posts': posts,
        'forums_counter': Forum.objects.count(),
        'categorys': Category.objects.all(),
        'category_slug': category_slug,
        'posts_n': posts,
    }

    # Render the template with the data
    return render(request, 'read_and_write.html', data)
