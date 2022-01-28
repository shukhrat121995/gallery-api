from django.shortcuts import render
from forceartsapi.models import Category, Wallpaper
from .forms import ContactForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    categories = Category.objects.all().order_by('rank')
    wallpapers = Wallpaper.objects.all().order_by('-upload_time')

    query = ""

    if request.method == 'GET':
        query = request.GET.get('query', None)
        if query:
            wallpapers = Wallpaper.objects.filter(
                Q(tags__name__in=[str(query)]) |
                Q(collection__title=str(query).lower())).distinct().order_by('-upload_time')
        else:
            query = ''

    paginator = Paginator(wallpapers, 50)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {
        'categories': categories,
        'page_obj': page_obj,
        'query': query
    })


def about(request):
    return render(request, 'about.html', {})


def characters(request):
    list_of_characters = Category.objects.filter(rank__lte=30).order_by('rank')
    return render(request, 'characters.html', {'characters': list_of_characters,})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            name = request.POST['full_name']
            messages.success(request, messages.SUCCESS)
            return render(request, 'contact.html', {'name': name})
        name = None
        messages.error(request, messages.ERROR)
        return render(request, 'contact.html', {'name': name})
    return render(request, 'contact.html', {})


def license(request):
    return render(request, 'license.html', {})

