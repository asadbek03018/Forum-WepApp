from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from forum.models import Forum, Thread, Post, Category
from creators.models import ForumCreators
from news.models import News
def home(request):
    """Home page"""
    if request.user.is_authenticated:
        if request.user.is_banned  == True:
            logout(request)
            return redirect('block_template')
        else:


            if request.method == 'POST':
                title = request.POST['u_title']
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

            else:
                # user = request.user
                # forum_creators = ForumCreators.objects.filter(user=user).first()
                # forum = forum_creators.forum if forum_creators else None
                # post_last = Post.objects.filter(thread__forum=forum).last() if forum else None
                filter_option = request.GET.get('filter', 'latest')

                if filter_option == 'latest':
                    forums = Forum.objects.order_by('-created_at')
                elif filter_option == 'popular':
                    forums = Forum.objects.order_by('-forum_views')
                elif filter_option == 'solved':
                    forums = Forum.objects.filter(status='solved').order_by('-created_at')
                elif filter_option == 'unsolved':
                    forums = Forum.objects.filter(status='unsolved').order_by('-created_at')
                elif filter_option == 'no_replies':
                    # forums = Forum.objects.filter(posts__isnull=True).order_by('-created_at')
                    forums = Forum.objects.order_by('-forum_views')
                else:
                    forums = Forum.objects.order_by('-created_at')
                data = {
                    'forums': forums,
                    # 'post_last': post_last,
                    'forums_counter': Forum.objects.count(),
                    'threads': Thread.objects.all(),
                    'categorys': Category.objects.all(),
                    'news': News.objects.all()
                }

            return render(request, 'index.html', data)
    else:
            filter_option = request.GET.get('filter', 'latest')

            if filter_option == 'latest':
                forums = Forum.objects.order_by('-created_at')
            elif filter_option == 'popular':
                forums = Forum.objects.order_by('-forum_views')
            elif filter_option == 'solved':
                forums = Forum.objects.filter(status='solved').order_by('-created_at')
            elif filter_option == 'unsolved':
                forums = Forum.objects.filter(status='unsolved').order_by('-created_at')
            elif filter_option == 'no_replies':
                forums = Forum.objects.order_by('-created_at')
            else:
                forums = Forum.objects.order_by('-created_at')

            # post_last = Post.objects.filter(thread__forum=forum).last() if forum else None

            data = {
                    'forums': forums,
                    # 'post_last': post_last,
                    'forums_counter': Forum.objects.count(),
                    'threads': Thread.objects.all(),
                    'categorys': Category.objects.all(),
                    'news': News.objects.all()
                }

            return render(request, 'index.html', data)
