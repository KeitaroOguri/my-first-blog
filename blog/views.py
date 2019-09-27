from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Comment, Reply


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "blog/signup.html"


class CommentView(generic.CreateView):
    """/comment/post_pk コメント投稿."""

    model = Comment
    fields = ("name", "text")
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        post_pk = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=post_pk)

        # 紐づく記事を設定する
        comment = form.save(commit=False)
        comment.target = post
        comment.save()

        # 記事詳細にリダイレクト
        return redirect("post_detail", pk=post_pk)


class ReplyView(generic.CreateView):
    """/reply/comment_pk 返信コメント投稿."""

    model = Reply
    fields = ("name", "text")
    template_name = "comment_form.html"

    def form_valid(self, form):
        comment_pk = self.kwargs["pk"]
        comment = get_object_or_404(Comment, pk=comment_pk)

        # 紐づくコメントを設定する
        reply = form.save(commit=False)
        reply.target = comment
        reply.save()

        # 記事詳細にリダイレクト
        return redirect("post_detail", pk=comment.target.pk)
