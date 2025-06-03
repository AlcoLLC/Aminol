from django.shortcuts import render
from django.db.models import Q
from django.utils.translation import get_language
from django.core.paginator import Paginator

# Import all your models
from about.models import AboutAminol, AboutSectionContent, Quality, QualityContent, WeGuarantee, Production, ProductionContent, DocumentsCertification, Sustainability, SustainabilityContent
from products.models import Product_group, Segments, Oil_Types, Viscosity, Liter, Product, ProductProperty
from career.models import Department, Job, JobApplication
from contact.models import Contact, ContactInfo
from faq.models import FAQ
from markets.models import Markets_Automotive, Markets_Automotive_Content, Markets_Industrial, Markets_Industrial_Content, Industries_Content, Markets_Shipping, Markets_Shipping_Content
from news.models import News, News_Content
from services.models import Aminol_Official_Dealer, Aminol_Official_Dealer_Content, Aminol_Labaratory, Aminol_Logistics


def search_view(request):
    query = request.GET.get('search', '').strip()
    results = []
    total_results = 0
    
    if query:
        current_language = get_language()
        is_english = current_language == 'en'
        
        if is_english:
            products = Product.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(features_benefits__icontains=query) |
                Q(application__icontains=query) |
                Q(recommendations__icontains=query) |
                Q(product_id__icontains=query) |
                Q(api__icontains=query) |
                Q(ilsac__icontains=query) |
                Q(acea__icontains=query) |
                Q(jaso__icontains=query)
            ).distinct()
        else:
            products = Product.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(features_benefits_translate__icontains=query) |
                Q(application_translate__icontains=query) |
                Q(recommendations_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(product_id__icontains=query)
            ).distinct()
        
        for product in products:
            title = product.title_translate if not is_english and product.title_translate else product.title
            description = product.description_translate if not is_english and product.description_translate else product.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': f'/product/{product.slug}/',
                'type': 'Product',
                'image': product.image.url if product.image else None
            })
        
        if is_english:
            product_groups = Product_group.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            product_groups = Product_group.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for group in product_groups:
            title = group.title_translate if not is_english and group.title_translate else group.title
            description = group.description_translate if not is_english and group.description_translate else group.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': f'/product/',
                'type': 'Product Group',
                'image': group.image.url if group.image else None
            })
        
        if is_english:
            news_items = News.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query),
                is_active=True
            ).distinct()
        else:
            news_items = News.objects.filter(
                Q(title_translate__icontains=query) |
                Q(content_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(content__icontains=query),
                is_active=True
            ).distinct()
        
        for news in news_items:
            title = news.title_translate if not is_english and news.title_translate else news.title
            content = news.content_translate if not is_english and news.content_translate else news.content
            results.append({
                'title': title,
                'description': content[:200] + '...' if content and len(content) > 200 else content or '',
                'url': f'/news/{news.id}/',
                'type': 'News',
                'image': news.image.url if news.image else None
            })
        
        if is_english:
            faqs = FAQ.objects.filter(
                Q(question__icontains=query) |
                Q(answer__icontains=query),
                is_active=True
            ).distinct()
        else:
            faqs = FAQ.objects.filter(
                Q(question_translate__icontains=query) |
                Q(answer_translate__icontains=query) |
                Q(question__icontains=query) |
                Q(answer__icontains=query),
                is_active=True
            ).distinct()
        
        for faq in faqs:
            question = faq.question_translate if not is_english and faq.question_translate else faq.question
            answer = faq.answer_translate if not is_english and faq.answer_translate else faq.answer
            results.append({
                'title': question,
                'description': answer[:200] + '...' if len(answer) > 200 else answer,
                'url': '/faq/',
                'type': 'FAQ',
                'image': None
            })
        
        jobs = Job.objects.filter(
            Q(title__icontains=query) |
            Q(job_description__icontains=query) |
            Q(requirements__icontains=query),
            is_active=True
        ).distinct()
        
        for job in jobs:
            results.append({
                'title': job.title,
                'description': job.job_description[:200] + '...' if len(job.job_description) > 200 else job.job_description,
                'url': f'/apply/{job.id}/',
                'type': 'Job',
                'image': None
            })
        
        if is_english:
            automotive_markets = Markets_Automotive.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            automotive_markets = Markets_Automotive.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for market in automotive_markets:
            title = market.title_translate if not is_english and market.title_translate else market.title
            description = market.description_translate if not is_english and market.description_translate else market.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/markets_automotive/',
                'type': 'Market - Automotive',
                'image': market.image.url if market.image else None
            })
        
        if is_english:
            industrial_markets = Markets_Industrial.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(industries_title__icontains=query) |
                Q(industries_description__icontains=query)
            ).distinct()
        else:
            industrial_markets = Markets_Industrial.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(industries_title_translate__icontains=query) |
                Q(industries_description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for market in industrial_markets:
            title = market.title_translate if not is_english and market.title_translate else market.title
            description = market.description_translate if not is_english and market.description_translate else market.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/markets_industrial/',
                'type': 'Market - Industrial',
                'image': market.image.url if market.image else None
            })
        
        if is_english:
            shipping_markets = Markets_Shipping.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(industries_title__icontains=query) |
                Q(industries_description__icontains=query)
            ).distinct()
        else:
            shipping_markets = Markets_Shipping.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(industries_title_translate__icontains=query) |
                Q(industries_description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for market in shipping_markets:
            title = market.title_translate if not is_english and market.title_translate else market.title
            description = market.description_translate if not is_english and market.description_translate else market.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/markets_shipping/',
                'type': 'Market - Shipping',
                'image': market.image.url if market.image else None
            })
        
        if is_english:
            about_sections = AboutSectionContent.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            about_sections = AboutSectionContent.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for section in about_sections:
            title = section.title_translate if not is_english and section.title_translate else section.title
            description = section.description_translate if not is_english and section.description_translate else section.description
            results.append({
                'title': title or 'About Section',
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/about/',
                'type': 'About',
                'image': section.image.url if section.image else None
            })
        
        if is_english:
            quality_contents = QualityContent.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            quality_contents = QualityContent.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for content in quality_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/about/?tab=quality/',
                'type': 'Quality',
                'image': content.image.url if content.image else None
            })

        if is_english:
            certifications_contents = DocumentsCertification.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            certifications_contents = DocumentsCertification.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

        for content in certifications_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/about/?tab=documents/',
                'type': 'Documents & Certifications',
                'image': content.image.url if content.image else None
            })
    
        
        if is_english:
            production_contents = ProductionContent.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            production_contents = ProductionContent.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for content in production_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/about/?tab=production/',
                'type': 'Production',
                'image': content.image.url if content.image else None
            })
        
        if is_english:
            sustainability_contents = SustainabilityContent.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            sustainability_contents = SustainabilityContent.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for content in sustainability_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/about/?tab=sustainability/',
                'type': 'Sustainability',
                'image': content.image.url if content.image else None
            })
        
        if is_english:
            dealer_services = Aminol_Official_Dealer.objects.filter(
                Q(title__icontains=query) |
                Q(title_description__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            dealer_services = Aminol_Official_Dealer.objects.filter(
                Q(title_translate__icontains=query) |
                Q(title_description_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for service in dealer_services:
            title = service.title_translate if not is_english and service.title_translate else service.title
            description = service.description_translate if not is_english and service.description_translate else service.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/service_aminol_dealer/',
                'type': 'Service',
                'image': service.image.url if service.image else None
            })
        
        if is_english:
            lab_services = Aminol_Labaratory.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            lab_services = Aminol_Labaratory.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for service in lab_services:
            title = service.title_translate if not is_english and service.title_translate else service.title
            description = service.description_translate if not is_english and service.description_translate else service.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/service_laboratory/',
                'type': 'Laboratory Service',
                'image': service.image.url if service.image else None
            })
        
        if is_english:
            logistics_services = Aminol_Logistics.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        else:
            logistics_services = Aminol_Logistics.objects.filter(
                Q(title_translate__icontains=query) |
                Q(description_translate__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        
        for service in logistics_services:
            title = service.title_translate if not is_english and service.title_translate else service.title
            description = service.description_translate if not is_english and service.description_translate else service.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if len(description) > 200 else description,
                'url': '/service_logistics/',
                'type': 'Logistics Service',
                'image': service.image.url if service.image else None
            })
        
        total_results = len(results)
        
        paginator = Paginator(results, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None
    
    context = {
        'query': query,
        'results': page_obj,
        'total_results': total_results,
    }
    
    return render(request, 'search.html', context)