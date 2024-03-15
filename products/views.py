from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, Category
from django.contrib import messages
from django.db.models import Q
from urllib.parse import unquote
from django.db.models.functions import Lower


def all_products(request):
    products = Product.objects.all()
    # for product in products:
    #     product.save()
    products = Product.objects.exclude(image_url__isnull=True).exclude(
        image_url__exact='').exclude(image_url__exact='[]').all()
    query = None
    categories = None
    sort = None
    direction = None

    if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category']
            # print(categories)
             # Decode the category parameter
            categories = unquote(categories).split('/')
            # print(categories)
            products = products.filter(category__name__in=categories)
            # print(products.query)
            categories = Category.objects.filter(name__in=categories)
            # print(categories.query)
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'
    # print(current_sorting)
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,

    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
