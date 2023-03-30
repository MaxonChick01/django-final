# blog/views.py
from django.views.generic import ListView, DetailView, FormView # new
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect



from .models import Post
from .forms import CommentForm


class CommentGet(DetailView): # new
    model = Post
    template_name = "post_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

class CommentPost(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = "post_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("post_detail", kwargs={"pk": self.object.pk})


class BlogListView(ListView):
    paginate_by = 3
    model = Post
    template_name = "home.html"


class BlogDetailView(DetailView, View): # new
    # model = Post
    # template_name = "post_detail.html"
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class BlogCreateView(CreateView): # new
    model = Post
    template_name = "post_new.html"
    fields = ["title", "author", "body"]

class BlogUpdateView(UpdateView): # new
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]

class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_pk"))
    if not post.likes.filter(id=request.user.id).exists():
        post.likes.add(request.user)
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)

    return HttpResponseRedirect(reverse("post_detail", kwargs={"pk": pk}))

    
    
def DislikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_pk"))
    if not post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.add(request.user)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)

    return HttpResponseRedirect(reverse("post_detail", kwargs={"pk": pk}))




