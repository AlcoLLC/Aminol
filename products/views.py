from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.text import slugify
from django.urls import reverse
from .models import Product, Product_group, Segments, Oil_Types, Viscosity, ProductProperty
from home.models import PartnerLogo, Gallery as GalleryImage, Supplier
import urllib.parse

def product_list(request, category_slug=None, segment_slug=None, oil_type_slug=None, viscosity_slug=None):
    products = Product.objects.all()    
    current_category = None
    current_segment = None
    current_oil_type = None
    current_viscosity = None    
    if category_slug:
        current_category = get_object_or_404(Product_group, slug=category_slug)
        products = products.filter(product_group=current_category)    
    if segment_slug:
        current_segment = get_object_or_404(Segments, slug=segment_slug)
        products = products.filter(segments=current_segment)    
    if oil_type_slug:
        current_oil_type = get_object_or_404(Oil_Types, slug=oil_type_slug)
        products = products.filter(oil_type=current_oil_type)    
    if viscosity_slug:
        current_viscosity = get_object_or_404(Viscosity, slug=viscosity_slug)
        products = products.filter(viscosity=current_viscosity)
    
    search_query = request.GET.get('search', '')
    if search_query:
        if not any([category_slug, segment_slug, oil_type_slug, viscosity_slug]):
            return redirect('products:product_search', search_term=urllib.parse.quote(search_query))
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(product_id__icontains=search_query)
        )    
    if request.GET.get('product_group') or request.GET.get('segments') or request.GET.get('oil_type') or request.GET.get('viscosity'):
        return handle_filter_redirect(request, category_slug, segment_slug, oil_type_slug, viscosity_slug)    
    products = products.select_related('product_group').order_by('order', 'product_group__order').distinct()    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)   
    context = get_product_context(
        page_obj, search_query, 
        current_category, current_segment, current_oil_type, current_viscosity,
        category_slug, segment_slug, oil_type_slug, viscosity_slug
    )    
    return render(request, 'product.html', context)

def product_search(request, search_term):
    search_query = urllib.parse.unquote(search_term)
    products = Product.objects.filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(product_id__icontains=search_query)
    ).select_related('product_group').order_by('order', 'product_group__order').distinct()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = get_product_context(page_obj, search_query)
    context['is_search'] = True
    context['search_term'] = search_term
    
    return render(request, 'product.html', context)

def handle_filter_redirect(request, category_slug=None, segment_slug=None, oil_type_slug=None, viscosity_slug=None):
    product_groups = request.GET.getlist('product_group')
    segments = request.GET.getlist('segments')
    oil_types = request.GET.getlist('oil_type')
    viscosities = request.GET.getlist('viscosity')
    product_groups = [pg for pg in product_groups if pg]
    segments = [s for s in segments if s]
    oil_types = [ot for ot in oil_types if ot]
    viscosities = [v for v in viscosities if v]
    url_kwargs = {}
    url_name = 'products:product_list'
    if len(product_groups) == 1:
        url_kwargs['category_slug'] = product_groups[0]
        url_name = 'products:product_list_by_category'
        if len(segments) == 1:
            url_kwargs['segment_slug'] = segments[0]
            url_name = 'products:product_list_by_category_segment'            
            if len(oil_types) == 1:
                url_kwargs['oil_type_slug'] = oil_types[0]
                url_name = 'products:product_list_by_category_segment_oil_type'                
                if len(viscosities) == 1:
                    url_kwargs['viscosity_slug'] = viscosities[0]
                    url_name = 'products:product_list_by_all_filters'                    
            elif len(viscosities) == 1:
                url_kwargs['viscosity_slug'] = viscosities[0]
                url_name = 'products:product_list_by_category_segment_viscosity'                
        elif len(oil_types) == 1:
            url_kwargs['oil_type_slug'] = oil_types[0]
            url_name = 'products:product_list_by_category_oil_type'            
            if len(viscosities) == 1:
                url_kwargs['viscosity_slug'] = viscosities[0]
                url_name = 'products:product_list_by_category_oil_type_viscosity'                
        elif len(viscosities) == 1:
            url_kwargs['viscosity_slug'] = viscosities[0]
            url_name = 'products:product_list_by_category_viscosity'            
    elif len(segments) == 1:
        url_kwargs['segment_slug'] = segments[0]
        url_name = 'products:product_list_by_segment'        
        if len(oil_types) == 1:
            url_kwargs['oil_type_slug'] = oil_types[0]
            url_name = 'products:product_list_by_segment_oil_type'            
            if len(viscosities) == 1:
                url_kwargs['viscosity_slug'] = viscosities[0]
                url_name = 'products:product_list_by_segment_oil_type_viscosity'                
        elif len(viscosities) == 1:
            url_kwargs['viscosity_slug'] = viscosities[0]
            url_name = 'products:product_list_by_segment_viscosity'            
    elif len(oil_types) == 1:
        url_kwargs['oil_type_slug'] = oil_types[0]
        url_name = 'products:product_list_by_oil_type'        
        if len(viscosities) == 1:
            url_kwargs['viscosity_slug'] = viscosities[0]
            url_name = 'products:product_list_by_oil_type_viscosity'            
    elif len(viscosities) == 1:
        url_kwargs['viscosity_slug'] = viscosities[0]
        url_name = 'products:product_list_by_viscosity'
    if not url_kwargs or len(product_groups) > 1 or len(segments) > 1 or len(oil_types) > 1 or len(viscosities) > 1:
        query_params = request.GET.copy()
        query_string = query_params.urlencode()
        if query_string:
            return redirect(f"/products/?{query_string}")
        return redirect('products:product_list')
    search_query = request.GET.get('search', '')
    if search_query:
        url_kwargs['search'] = search_query    
    try:
        return redirect(url_name, **url_kwargs)
    except:
        query_params = request.GET.copy()
        query_string = query_params.urlencode()
        if query_string:
            return redirect(f"/products/?{query_string}")
        return redirect('products:product_list')

def get_product_context(page_obj, search_query='', current_category=None, current_segment=None, 
                       current_oil_type=None, current_viscosity=None, category_slug=None, 
                       segment_slug=None, oil_type_slug=None, viscosity_slug=None):
    
    product_groups = Product_group.objects.all().order_by('order')
    segments = Segments.objects.all()
    oil_types = Oil_Types.objects.all()
    viscosity_options = Viscosity.objects.all()
    images = GalleryImage.objects.all().order_by('order')
    partner_logos = PartnerLogo.objects.all()
    supplier_logos = Supplier.objects.all()
    
    selected_product_groups = [category_slug] if category_slug else []
    selected_segments = [segment_slug] if segment_slug else []
    selected_oil_types = [oil_type_slug] if oil_type_slug else []
    selected_viscosity = [viscosity_slug] if viscosity_slug else []
    
    return {
        'products': page_obj,
        'page_obj': page_obj,
        'product_groups': product_groups,
        'segments': segments,
        'oil_types': oil_types,
        'viscosity_options': viscosity_options,
        'search_query': search_query,
        'selected_product_groups': selected_product_groups,
        'selected_segments': selected_segments,
        'selected_oil_types': selected_oil_types,
        'selected_viscosity': selected_viscosity,
        'images': images,
        'partner_logos': partner_logos,
        'supplier_logos': supplier_logos,
        'current_category': current_category,
        'current_segment': current_segment,
        'current_oil_type': current_oil_type,
        'current_viscosity': current_viscosity,
        'category_slug': category_slug,
        'segment_slug': segment_slug,
        'oil_type_slug': oil_type_slug,
        'viscosity_slug': viscosity_slug,
    }

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    properties = ProductProperty.objects.filter(product=product).order_by('order', 'id')
    available_liters = product.liters.all().order_by('volume')
    context = {
        'product': product,
        'available_liters': available_liters,
        'properties': properties,
    }

    return render(request, 'product_detail.html', context)

def product_properties_ajax(request, product_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        product = get_object_or_404(Product, id=product_id)
        properties = ProductProperty.objects.filter(product=product).order_by('order', 'id')
        properties_data = []
        for prop in properties:
            properties_data.append({
                'property_name': prop.property_name,
                'unit': prop.unit or '',
                'test_method': prop.test_method,
                'typical_value': prop.typical_value,
            })
        return JsonResponse({
            'success': True,
            'properties': properties_data,
            'product_title': product.title,
            'pds_url': product.pds_url or '',
            'sds_url': product.sds_url or '',
        })

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def legacy_product_redirect(request):
    product_name = request.GET.get('title')    
    if not product_name:
        return handle_filter_redirect(request)
    possible_slug = slugify(product_name)
    try:
        product = get_object_or_404(Product, slug=possible_slug)
        return redirect('products:product_detail', slug=product.slug, permanent=True)
    except:
        return redirect('products:product_list', permanent=True)
def seo_url_context(request):
    return {
        'generate_category_url': lambda category_slug: reverse('products:product_list_by_category', kwargs={'category_slug': category_slug}),
        'generate_segment_url': lambda segment_slug: reverse('products:product_list_by_segment', kwargs={'segment_slug': segment_slug}),
        'generate_oil_type_url': lambda oil_type_slug: reverse('products:product_list_by_oil_type', kwargs={'oil_type_slug': oil_type_slug}),
        'generate_viscosity_url': lambda viscosity_slug: reverse('products:product_list_by_viscosity', kwargs={'viscosity_slug': viscosity_slug}),
        'generate_category_segment_url': lambda category_slug, segment_slug: reverse('products:product_list_by_category_segment', kwargs={'category_slug': category_slug, 'segment_slug': segment_slug}),
        'generate_search_url': lambda search_term: reverse('products:product_search', kwargs={'search_term': urllib.parse.quote(search_term)}),
    }