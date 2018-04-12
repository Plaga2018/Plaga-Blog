from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from blog.models import Post,Comment
from django.urls import reverse_lazy
from blog.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    '''
    a query on my model
    grab a post model and objects there and filter based on publisheddate__lte("less than or equal too")
    the current time. then order by published_date.  -published (descending because of the "-")

    This is called a field lookup in Django documentation.
    https://docs.djangoproject.com/en/1.10/topics/db/queries

    SQL equevalent
    # SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';

    '''
    def get_queryset(self):
        return Post.object.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

# creates a new post with login required
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


# updates your post with login required
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

# This is the draft that is stored before they are submitted
class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'

    redirect_field_name = 'blog/post_list'
    model = Post

# Checking for no publish_date
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')



##################################################################
##################################################################
#Publish View
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish
    return redirect('post_detail')

#Comment views

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.Post)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    # pulled from the class Comment.approve() function
    comment.approve()
    #this comes from the Comment then to the Post
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    #extra variable so we dont delete before removing
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
