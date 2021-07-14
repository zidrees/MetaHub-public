from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin

from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
# Create your views here.
from .models import Category
from .walmart import scrape_walmart_data
from .target import scrape_target_data

from django.views.decorators.cache import cache_page
def product_search(request, category_slug=None):
    form = SearchForm()
    cart_product_form = CartAddProductForm()
    category_walmart = []
    category_target = []
    query = None
    walmart_data = []
    target_data = []
    categories = Category.objects.all()
    if category_slug:
        category = category_slug
        category_walmart = scrape_walmart_data(category)
        category_target = scrape_target_data(category)

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            walmart_data = scrape_walmart_data(query)

            target_data = scrape_target_data(query)
            # # print(target_data)
    # if category_slug:
    #     category = self.kwargs['category_name'])
    #     context['category'] = self.model.objects.filter(category=category)

    return render(request, 'product.html',
                  {'form': form,
                   'cart_product_form': cart_product_form,
                   'query': query,
                   'walmart_data': walmart_data,
                   'target_data': target_data,
                   'categories': categories,
                   'category_target': category_target,
                   'category_walmart': category_walmart,

                   })


class ProductListView(FormMixin, TemplateView):
    # model = Post
    # context_object_name = 'posts'
    template_name = 'product.html'
    form_class = SearchForm
    cart_product_form = CartAddProductForm()
    paginate_by = 4

    def get_context_data(self, **kwargs):

        category_slug = self.kwargs.get('category_slug')
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cart_product_form'] = self.cart_product_form

        if category_slug:

            category = self.kwargs['category_slug']
            context['category'] = category
            context['category_walmart_data'] = scrape_walmart_data(category)

            context['category_target_data'] = scrape_target_data(category)

        else:

            if 'query' in self.request.GET:
                form = SearchForm(self.request.GET)
                if form.is_valid():
                    query = form.cleaned_data['query']
                    context['query'] = query
                    context['walmart_data'] = scrape_walmart_data(query)
                    context['target_data'] = scrape_target_data(query)

        return context
