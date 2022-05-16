from re import search
from django.shortcuts import render , get_object_or_404
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from .models import Post , comment
from django.views.generic import ListView
from .forms import CommentForms , SearchForm ,EmailPostForm
from django.http import HttpResponseRedirect
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector , SearchQuery , SearchRank
from django.core.mail import send_mail
# Create your views here.


def post_list(request,tag_slug=None):
    posts = Post.objects.filter(status="published")
    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts,8)
    page =request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts =paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{"posts":posts,"tag":tag})


#class PostListView(ListView):
  #  queryset = Post.objects.filter(status="published")
   # paginate_by = 2
   # context_object_name ="posts"
  #  template_name = "blog/post/list.html"


def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post , publish__year=year ,publish__month=month , publish__day=day)
    comment_post =post.comment.filter(active=True)
    
    post_tag_id =post.tags.values_list('id',flat=True)
    similar_post =Post.objects.filter(status ="published",tags__in=post_tag_id).exclude(id=post.id)
    similar_post=similar_post.annotate(same_tags=Count('tags')).order_by("-same_tags","publish")
    
    if request.method == 'POST':
        comment_forms =CommentForms(data=request.POST)
        if comment_forms.is_valid():
            new_comment = comment_forms.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        comment_forms = CommentForms()
    return render(request,'blog/post/detail.html',{"post":post,"form":comment_forms,"comment":comment_post,"same_tag":similar_post})

#search
def post_search(request):
    form =SearchForm(request.GET)
    query = None
    results = []
    if 'query' in request.GET:
        form =SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            search_vector = SearchVector('title', weight ='A') + SearchVector('body' , weight='C')
            search_query = SearchQuery(query)

            results =Post.objects.annotate(search=search_vector , rank =SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')
    return render(request,'blog/post/search.html',{'form':form , 'query':query , 'results':results})

#share post
def post_share(request,post_id):
    post = get_object_or_404(Post , id = post_id , status = "published")
    
    if request.method =='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd =form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommend you"
            message = f"{post.title} in {post_url} and {cd['comment']}"
            send_mail(
                subject,message,"nima.mohammadi.021@gmail.com",
                [cd['to']]
            )
    else:
        form = EmailPostForm()  
    
    return render(request,'blog/post/share.html' , {'post':post , 'form':form})
