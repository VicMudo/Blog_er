from django.shortcuts import render

from .models import  SearchQuery
from blog.models import Post

def search_view(request, *args, **kwargs):
    query = request.GET.get('q', None)

    user = None
    if request.user.is_authenticated:
        user = request.user
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        search_list = Post.objects.search(query=query)
       # context['search_list'] = search_list
    context = {
        "query": query,
        "search_list": search_list
    }
    return render(request, 'searches/search.html', context)