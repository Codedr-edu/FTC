from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Bio(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    description = models.TextField()
    avatar = models.ImageField(upload_to="images/")
    rank = models.CharField(max_length=1000, null=True, blank=True)
    facebook = models.TextField(null=True, blank=True)
    ig = models.TextField(null=True, blank=True)
    slug = models.SlugField()


class Bio_title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    bio = models.ForeignKey(Bio, on_delete=models.CASCADE, related="bio_title")


class Blog(models.Model):
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="blog_user")
    title = models.CharField(max_length=1000)
    description = models.TextField()
    cover = models.ImageField(upload_to="images/blog/cover/")
    like = models.ManyToManyField(
        Bio, on_delete=models.CASCADE, related_name="like_blog")
    dislike = models.ManyToManyField(
        Bio, on_delete=models.CASADE, related_name="dislike_blog")
    comment_counter = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()


class Blog_tag(models.Model):
    name = models.CharField(max_length=100)
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="blog_tag")


class Comment_blog(models.Model):
    user = models.CharField(max_length=1000)
    content = models.TextField()
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comment_post")
    like = models.ManyToManyField(
        Bio, on_delete=models.CASCADE, related_name="like_post")
    dislike = models.ManyToManyField(
        Bio, on_delete=models.CASADE, related_name="dislike_post")
    datetime = models.DateTimeField(auto_now_add=True)


class Blog_images(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="blog_images")
    image = models.ImageField(upload_to="images/blog/")


class History(models.Model):
    time = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.ImageField()


class Roadmap(models.Model):
    time = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.ImageField()


class Carousel_images(models.Model):
    image = models.ImageField(upload_to="images/carousel/")


class Album_images(models.Model):
    image = models.ImageField(upload_to="images/album/")


class development_team(models.Model):
    name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/creator/")
    title = models.TextField()


class Apply(models.Model):
    name = models.TextField()
    class_code = models.CharField(max_length=5)
    cover_letter = models.TextField()
