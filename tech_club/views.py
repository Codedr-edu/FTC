from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.apps import AppConfig
from django.db.models import Q
from django.template.defaultfilters import slugify  # new

# Create your views here.


def index(request):
    carousel = Carousel_images.objects.all()
    album = Album_images.objects.all()
    blog = Blog.objects.all()
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
    context = {"carousels": carousel,
               "albums": album[0:5], "blogs": blog[0:3], "bio": bio}
    return render(request, "index.html", context)


def blog_list(request):
    blog = Blog.objects.all()
    context = {"blogs": blog}
    return render(request, "blog/list.html", context)


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("check")
            else:
                return redirect("all_error")
    else:
        return redirect("check")


def check(request):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        if not bio:
            if request.method == "POST":
                description = request.POST.get("description")
                avatar = request.FILE.get("avatar")
                thumbnail = request.FILE.get("thumbnail")
                slug = slugify(request.user.username)

                bio = Bio(user=request.user, description=description,
                          avatar=avatar, thumbnail=thumbnail, slug=slug)
                bio.save()
                return render("post")
        else:
            return render("post")
    return render(request, "accounts/check.html")


def add_user(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                username = request.POST.get("username")
                last_name = request.POST.get("last_name")
                first_name = request.POST.get("first_name")
                email = request.POST.get("email")
                password = request.POST.get("password")

                user = User.objects.get(username=username, email=email)
                if user:
                    return redirect("account_info", id=user.id)
                else:
                    user = User.objects.create(
                        username=username, email=email, last_name=last_name, first_name=first_name, password=password)
                    user.save()
                    user = User.objects.get(
                        username=username, email=email, last_name=last_name, first_name=first_name, password=password)
                    return redirect("account_info", id=user.id)
        else:
            return redirect("index")
    else:
        return redirect("index")


def account_info(request, slug):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = Bio.objects.filter(slug=slug).first()
            context = {"user": user}
        else:
            return redirect("index")
    else:
        return redirect("index")
    return render(request, "accounts/info.html", context)


def user_info(request, slug):
    bio = Bio.objects.filter(slug=slug).first()
    blog = Blog.objects.filter(user=bio).all()
    context = {"user": bio, "blogs": blog[:3]}
    return render(request, "accounts/user_info.html", context)


def blog_view(request, slug):
    blog = Blog.objects.filter(slug=slug).first()
    comment = Comment_blog.objects.filter(blog=blog).all()
    images = Blog_images.objects.filter(blog=blog).all()
    if blog:
        context = {"blog": blog, "comments": comment, "images": images}
    else:
        return redirect("index")
    return render(request, "blog/view.html", context)

# create


def comment_blog(request, slug):
    blog = Blog.objects.filter(slug=slug).first()
    if blog:
        if request.method == "POST":
            if not request.user.is_authenticated:
                user = request.POST.get("user")
            else:
                user = str(request.user.last_name) + " " + \
                    str(request.user.first_name)
            content = request.POST.get("content")

            comment = Comment_blog(user=user, content=content, blog=blog)
            comment.save()
            return redirect("blog_view", slug=slug)
    else:
        return redirect("index")


def create_blog(request):
    if request.user.is_authenticated and request.user.is_staff:
        bio = Bio.objects.filter(user=request.user).first()
        if bio:
            if request.method == "POST":
                title = request.POST.get("title")
                content = request.POST.get("content")
                cover = request.FILE.get("cover")
                images = request.FILES.getlist("images")
                tags = request.POST.get("tags").split(",")
                slug = slugify(title)

                sql = Blog(title=title, description=content,
                           cover=cover, slug=slug)
                sql.save()

                blog = Blog.objects.filter(
                    title=title, description=content, cover=cover, slug=slug).first()

                for tag in tags:
                    blog_tag = Blog_tag(name=tag, blog=blog)
                    blog_tag.save()

                for image in images:
                    img = Blog_images(image=image, blog=blog)
                    img.save()

                return redirect("blog_view", id=blog.id)
        else:
            return redirect("index")
    else:
        return redirect("index")
    return render(request, "blog/create.html")


def album(request):
    images = Album_images.objects.all()
    context = {"images": images}
    return render(request, "album.html", context)


def roadmaps(request):
    members = Roadmap.objects.all()
    context = {"roadmaps": members}
    return render(request, "roadmaps.html", context)


def timelines(request):
    members = History.objects.all()
    context = {"timelines": members}
    return render(request, "timelines.html", context)

# update


def update_comment_blog(request, slug):
    blog = Comment_blog.objects.filter(slug=slug).first()
    if blog:
        if request.method == "POST":
            if not request.user.is_authenticated:
                blog.user = request.POST.get("user")
            else:
                blog.user = str(request.user.last_name) + " " + \
                    str(request.user.first_name)
            blog.content = request.POST.get("content")

            blog.save()
            return redirect("blog_view", slug=slug)
    else:
        return redirect("index")


def update_blog(request, slug):
    if request.user.is_authenticated and request.user.is_staff:
        blog = Blog.objects.filter(slug=slug).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio:
            if request.method == "POST":
                blog.title = request.POST.get("title")
                blog.content = request.POST.get("content")
                blog.cover = request.FILE.get("cover")
                images = request.FILES.getlist("images")
                tags = request.POST.get("tags").split(",")

                blog.save()

                for tag in tags:
                    blog_tag = Blog_tag(name=tag, blog=blog)
                    blog_tag.save()

                for image in images:
                    img = Blog_images(image=image, blog=blog)
                    img.save()

                return redirect("blog_view", id=blog.id)
        else:
            return redirect("index")
    else:
        return redirect("index")

# like


def like_blog(request, slug):
    if request.user.is_authenticated:
        post = Blog.objects.filter(slug=slug).first()
        bio = Bio.objects.filter(user=request.user).first()
        if not bio in post.like.all():
            post.like.add(bio)
            return redirect("read_blog", slug=slug)
        else:
            post.like.remove(bio)
            return redirect("read_blog", slug=slug)
    else:
        return redirect("index")


def like_comment_blog(request, slug):
    if request.user.is_authenticated:
        post = Comment_blog.objects.filter(slug=slug).first()
        bio = Bio.objects.filter(user=request.user).first()
        if not bio in post.like.all():
            post.like.add(bio)
            return redirect("read_blog", slug=slug)
        else:
            post.like.remove(bio)
            return redirect("read_blog", slug=slug)
    else:
        return redirect("index")


# dislike


def dislike_blog(request, slug):
    if request.user.is_authenticated:
        post = Blog.objects.filter(slug=slug).first()
        bio = Bio.objects.filter(user=request.user).first()
        if not bio in post.dislike.all():
            post.dislike.add(bio)
            return redirect("read_blog", slug=slug)
        else:
            post.dislike.remove(bio)
            return redirect("read_blog", slug=slug)
    else:
        return redirect("index")


def dislike_comment_blog(request, slug):
    if request.user.is_authenticated:
        post = Comment_blog.objects.filter(slug=slug).first()
        bio = Bio.objects.filter(user=request.user).first()
        if not bio in post.dislike.all():
            post.dislike.add(bio)
            return redirect("read_blog", slug=slug)
        else:
            post.dislike.remove(bio)
            return redirect("read_blog", slug=slug)
    else:
        return redirect("index")

# apply


def apply(request):
    if request.method == "POST":
        name = request.POST.get("name")
        class_code = request.POST.get("class_code")
        cover_letter = request.POST.get("cover_letter")

        app = Apply(name=name, class_code=class_code,
                    cover_letter=cover_letter)
        app.save()
        app = Apply.objects.filter(
            name=name, class_code=class_code, cover_letter=cover_letter).first()
        return redirect("apply_success", id=app.id)


def apply_success(request, slug):
    app = Apply.objects.filter(slug=slug).first()
    if app:
        context = {"applies": apply}
    else:
        return redirect("apply_error")
    return render(request, "apply/success.html", context)


def apply_error(request):
    return render(request, "apply/error.html")

# bio check


def bio_list_view(request):
    members = Bio.objects.all()
    context = {"members": members}
    return render(request, "member/list.html", context)


def bio_view(request, slug):
    members = Bio.objects.filter(slug=slug).first()
    title = Bio_title.objects.filter(bio=members).all()
    context = {"member": members, "titles": title}
    return render(request, "member/view.html", context)
