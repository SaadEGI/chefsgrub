import random

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddToCartForm
from .models import Category, Product
from apps.vendor.models import Vendor

from apps.cart.cart import Cart


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'product/search.html', {'products': products, 'query': query})


def product(request, category_slug, product_slug):
    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    imagesstring = '{"thumbnail": "%s","trendingimage": "%s", "image": "%s", "id": "mainimage"},' % (
    product.get_thumbnail(), product.get_trendingimage(), product.image.url)

    for image in product.images.all():
        imagesstring += ('{"thumbnail": "%s","trendingimage": "%s" ,"image": "%s", "id": "%s"},' % (
        image.get_thumbnail(),image.get_trendingimage(), image.image.url, image.id))

    print(imagesstring)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = 1

            # form.cleaned_data['quantity']

            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, 'The product was added to the cart')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)
    else:
        form = AddToCartForm()

    similar_products = list(product.category.products.exclude(id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    context = {
        'form': form,
        'product': product,
        'similar_products': similar_products,
        'imagesstring': "[" + imagesstring.rstrip(',') + "]"
    }

    return render(request, 'product/product.html', context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    vendors = Vendor.objects.all()
    CategoryVendor = []
    AllCategoryVendor = []

    for vendor in vendors:
        for product in vendor.products.all():
            if product.category not in AllCategoryVendor:
                AllCategoryVendor.append(product.category)
            if product.category==category:

                CategoryVendor.append(vendor)
                break;







    return render(request, 'product/category.html', {'AllCategoryVendor':AllCategoryVendor,'CategoryVendor':CategoryVendor,'category': category})
