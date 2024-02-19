from django.urls import path
from . import views

urlpatterns = [
    # index
    path('', views.index, name="index"),
    # authenticate
    path('accounts/login', views.Login, name="a_login"),
    path('logout/', views.log_out, name="log_out"),
    # like
    path('like/blog/<slug:slug>', views.like_blog, name="like_blog"),
    path('like/post/<slug:slug>', views.like_post, name="like_post"),
    path('like/comment/post/<slug:slug>',
         views.like_comment_post, name="like_comment_post"),
    path('like/comment/blog/<slug:slug>',
         views.like_comment_blog, name="like_comment_blog"),
    # dislike
    path('dislike/blog/<slug:slug>',
         views.dislike_blog, name="dislike_blog"),
    path('dislike/post/<slug:slug>', views.dislike_post, name="dislike_post"),
    path('dislike/comment/post/<slug:slug>',
         views.like_comment_post, name="like_comment_post"),
    path('dislike/comment/blog/<slug:slug>',
         views.like_comment_blog, name="like_comment_blog"),
    # comment
    path('comment/post/<slug:slug>', views.comment_post, name="comment_post"),
    path('comment/blog/<slug:slug>',
         views.comment_blog, name="comment_blog"),
    # read
    path("view/blog/<slug:slug>", views.blog_view, name="blog_view"),
    path("view/question/<slug:slug>",
         views.question_view, name="question_view"),
    # create
    path("create/post/", views.post_create, name="create_post"),
    path("create/blog/", views.blog_create, name="create_blog"),
    # update
    path("update/post/<slug:slug>", views.update_post, name="update_post"),
    path("update/blog/<slug:slug>", views.update_blog, name="update_blog"),
    path("update/comment/post/<slug:slug>",
         views.update_comment_post, name="update_comment_post"),
    path("update/comment/blog/<slug:slug>",
         views.update_comment_blog, name="update_comment_blog"),
    # delete
    path("delete/post/<slug:slug>", views.delete_post, name="delete_post"),
    path("delete/blog/<slug:slug>", views.delete_blog, name="delete_blog"),
    path("delete/comment/post/<slug:slug>",
         views.delete_comment_post, name="update_comment_post"),
    path("delete/comment/blog/<slug:slug>",
         views.delete_comment_blog, name="update_comment_blog"),
    # user
    path("user/<slug:slug>", views.user_profile, name="user_profile"),
    path("your/profile/", views.your_profile, name="your_profile"),
    path("delete/profile/", views.delete_user, name="delete_profile"),
    # list_view
    path("post/", views.post, name="post"),
    path("blog/", views.blog_list, name="blog"),
    path("timeline/", views.timelines, name="timelines"),
    path("roadmap/", views.roadmaps, name="roadmaps"),
    path("album/", views.album, name="album"),
    path("member/", views.Member, name="member"),
    # apply
    path("apply/", views.apply, name="apply"),
    path("apply/success/<slug:slug>", views.apply_success, name="apply_success"),
    path("apply/error/", views.apply_error, name="apply_error"),
]
