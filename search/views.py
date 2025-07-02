from django.shortcuts import render
from django.db.models import Q
from django.utils.translation import get_language
from django.core.paginator import Paginator
import re

# Import all your models
from about.models import AboutAminol, AboutSectionContent, Quality, QualityContent, WeGuarantee, Production, ProductionContent, DocumentsCertification, Sustainability, SustainabilityContent
from products.models import Product_group, Segments, Oil_Types, Viscosity, Liter, Product, ProductProperty
from career.models import Department, Job, JobApplication
from contact.models import Contact, ContactInfo
from faq.models import FAQ
from markets.models import Markets_Automotive, Markets_Automotive_Content, Markets_Industrial, Markets_Industrial_Content, Industries_Content, Markets_Shipping, Markets_Shipping_Content
from news.models import News, News_Content
from services.models import Aminol_Official_Dealer, Aminol_Official_Dealer_Content, Aminol_Labaratory, Aminol_Logistics


def create_search_queries(query):
    """
    Create multiple search queries from the input:
    1. Full query
    2. Individual words
    3. Partial matches for each word
    """
    queries = []
    
    # Add the full query
    queries.append(query.strip())
    
    # Split by spaces and add individual words (minimum 2 characters)
    words = [word.strip() for word in query.split() if len(word.strip()) >= 2]
    queries.extend(words)
    
    return queries


def build_search_q(query, fields):
    """
    Build a Q object for searching across multiple fields with partial matching
    """
    q_objects = Q()
    search_queries = create_search_queries(query)
    
    for field in fields:
        for search_term in search_queries:
            q_objects |= Q(**{f"{field}__icontains": search_term})
    
    return q_objects


def search_view(request):
    query = request.GET.get('search', '').strip()
    results = []
    total_results = 0
    
    if query and len(query) >= 2:  # Minimum 2 characters for search
        current_language = get_language()
        is_english = current_language == 'en'
        
        # Search Products
        if is_english:
            product_fields = ['title', 'description', 'features_benefits', 'application', 
                            'recommendations', 'product_id', 'api', 'ilsac', 'acea', 'jaso']
        else:
            product_fields = ['title_translate', 'description_translate', 'features_benefits_translate', 
                            'application_translate', 'recommendations_translate', 'title', 'description', 'product_id']
        
        products = Product.objects.filter(build_search_q(query, product_fields)).distinct()
        
        for product in products:
            title = product.title_translate if not is_english and product.title_translate else product.title
            description = product.description_translate if not is_english and product.description_translate else product.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': f'/product/{product.slug}/',
                'type': 'Product',
                'image': product.image.url if product.image else None
            })
        
        # Search Product Groups
        if is_english:
            group_fields = ['title', 'description']
        else:
            group_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        product_groups = Product_group.objects.filter(build_search_q(query, group_fields)).distinct()
        
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
        
        # Search Segments
        if is_english:
            segment_fields = ['title']
        else:
            segment_fields = ['title_translate', 'title']
        
        segments = Segments.objects.filter(build_search_q(query, segment_fields)).distinct()
        
        for segment in segments:
            title = segment.title_translate if not is_english and segment.title_translate else segment.title
            results.append({
                'title': title,
                'description': f'Product Segment: {title}',
                'url': f'/product/?segment={segment.slug}',
                'type': 'Product Segment',
                'image': None
            })
        
        # Search Oil Types
        if is_english:
            oil_type_fields = ['title']
        else:
            oil_type_fields = ['title_translate', 'title']
        
        oil_types = Oil_Types.objects.filter(build_search_q(query, oil_type_fields)).distinct()
        
        for oil_type in oil_types:
            title = oil_type.title_translate if not is_english and oil_type.title_translate else oil_type.title
            results.append({
                'title': title,
                'description': f'Oil Type: {title}',
                'url': f'/product/?oil_type={oil_type.slug}',
                'type': 'Oil Type',
                'image': None
            })
        
        # Search Viscosity
        viscosities = Viscosity.objects.filter(build_search_q(query, ['title'])).distinct()
        
        for viscosity in viscosities:
            results.append({
                'title': viscosity.title,
                'description': f'Viscosity: {viscosity.title}',
                'url': f'/product/?viscosity={viscosity.slug}',
                'type': 'Viscosity',
                'image': None
            })
        
        # Search Product Properties
        if is_english:
            property_fields = ['property_name', 'test_method', 'typical_value']
        else:
            property_fields = ['property_name_translate', 'test_method_translate', 
                             'typical_value_translate', 'property_name', 'test_method', 'typical_value']
        
        product_properties = ProductProperty.objects.filter(build_search_q(query, property_fields)).distinct()
        
        for prop in product_properties:
            property_name = prop.property_name_translate if not is_english and prop.property_name_translate else prop.property_name
            results.append({
                'title': f'{prop.product.title} - {property_name}',
                'description': f'Property: {property_name}, Test Method: {prop.test_method}, Value: {prop.typical_value}',
                'url': f'/product/{prop.product.slug}/',
                'type': 'Product Property',
                'image': None
            })
        
        # Search News
        if is_english:
            news_fields = ['title', 'content']
        else:
            news_fields = ['title_translate', 'content_translate', 'title', 'content']
        
        news_items = News.objects.filter(
            build_search_q(query, news_fields),
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
        
        # Search News Content
        if is_english:
            news_content_fields = ['description']
        else:
            news_content_fields = ['description_translate', 'description']
        
        news_contents = News_Content.objects.filter(build_search_q(query, news_content_fields)).distinct()
        
        for content in news_contents:
            description = content.description_translate if not is_english and content.description_translate else content.description
            news_title = content.news.title_translate if not is_english and content.news.title_translate else content.news.title
            results.append({
                'title': news_title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': f'/news/{content.news.id}/',
                'type': 'News',
                'image': content.image.url if content.image else None
            })
        
        # Search FAQ
        if is_english:
            faq_fields = ['question', 'answer']
        else:
            faq_fields = ['question_translate', 'answer_translate', 'question', 'answer']
        
        faqs = FAQ.objects.filter(
            build_search_q(query, faq_fields),
            is_active=True
        ).distinct()
        
        for faq in faqs:
            question = faq.question_translate if not is_english and faq.question_translate else faq.question
            answer = faq.answer_translate if not is_english and faq.answer_translate else faq.answer
            results.append({
                'title': question,
                'description': answer[:200] + '...' if answer and len(answer) > 200 else answer or '',
                'url': '/faq/',
                'type': 'FAQ',
                'image': None
            })
        
        # Search Jobs
        jobs = Job.objects.filter(
            build_search_q(query, ['title', 'job_description', 'requirements']),
            is_active=True
        ).distinct()
        
        for job in jobs:
            results.append({
                'title': job.title,
                'description': job.job_description[:200] + '...' if job.job_description and len(job.job_description) > 200 else job.job_description or '',
                'url': f'/career/apply/{job.id}/',
                'type': 'Job',
                'image': None
            })
        
        # Search Departments
        departments = Department.objects.filter(
            build_search_q(query, ['name']),
            is_active=True
        ).distinct()
        
        for dept in departments:
            results.append({
                'title': dept.name,
                'description': f'Department: {dept.name}',
                'url': '/career/',
                'type': 'Department',
                'image': None
            })
        
        # Search Markets Automotive
        if is_english:
            automotive_fields = ['title', 'description']
        else:
            automotive_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        automotive_markets = Markets_Automotive.objects.filter(build_search_q(query, automotive_fields)).distinct()
        
        for market in automotive_markets:
            title = market.title_translate if not is_english and market.title_translate else market.title
            description = market.description_translate if not is_english and market.description_translate else market.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/markets/automotive/',
                'type': 'Market - Automotive',
                'image': market.image.url if market.image else None
            })
        
        # Search Markets Automotive Content
        if is_english:
            auto_content_fields = ['title', 'description']
        else:
            auto_content_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        automotive_contents = Markets_Automotive_Content.objects.filter(build_search_q(query, auto_content_fields)).distinct()
        
        for content in automotive_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/markets/automotive/',
                'type': 'Market - Automotive',
                'image': content.image.url if content.image else None
            })
        
        # Search Markets Industrial
        if is_english:
            industrial_fields = ['title', 'description', 'industries_title', 'industries_description']
        else:
            industrial_fields = ['title_translate', 'description_translate', 'industries_title_translate', 
                               'industries_description_translate', 'title', 'description']
        
        industrial_markets = Markets_Industrial.objects.filter(build_search_q(query, industrial_fields)).distinct()
        
        for market in industrial_markets:
            title = market.title_translate if not is_english and market.title_translate else market.title
            description = market.description_translate if not is_english and market.description_translate else market.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/markets/industrial/',
                'type': 'Market - Industrial',
                'image': market.image.url if market.image else None
            })
        
        # Search Markets Industrial Content
        if is_english:
            ind_content_fields = ['title', 'description']
        else:
            ind_content_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        industrial_contents = Markets_Industrial_Content.objects.filter(build_search_q(query, ind_content_fields)).distinct()
        
        for content in industrial_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/markets/industrial/',
                'type': 'Market - Industrial',
                'image': content.image.url if content.image else None
            })
        
        # Search Industries Content
        if is_english:
            industry_fields = ['title']
        else:
            industry_fields = ['title_translate', 'title']
        
        industries_contents = Industries_Content.objects.filter(build_search_q(query, industry_fields)).distinct()
        
        for content in industries_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            results.append({
                'title': title,
                'description': f'Industry: {title}',
                'url': '/markets/industrial/',
                'type': 'Industry',
                'image': None
            })
        
        # Search Markets Shipping
        if is_english:
            shipping_fields = ['title', 'description', 'industries_title', 'industries_description']
        else:
            shipping_fields = ['title_translate', 'description_translate', 'industries_title_translate', 
                             'industries_description_translate', 'title', 'description']
        
        shipping_markets = Markets_Shipping.objects.filter(build_search_q(query, shipping_fields)).distinct()
        
        for market in shipping_markets:
            title = market.title_translate if not is_english and market.title_translate else market.title
            description = market.description_translate if not is_english and market.description_translate else market.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/markets/shipping/',
                'type': 'Market - Shipping',
                'image': market.image.url if market.image else None
            })
        
        # Search Markets Shipping Content
        if is_english:
            ship_content_fields = ['title', 'description']
        else:
            ship_content_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        shipping_contents = Markets_Shipping_Content.objects.filter(build_search_q(query, ship_content_fields)).distinct()
        
        for content in shipping_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/markets/shipping/',
                'type': 'Market - Shipping',
                'image': content.image.url if content.image else None
            })
        
        # Search About Sections
        if is_english:
            about_fields = ['title', 'description']
        else:
            about_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        about_sections = AboutSectionContent.objects.filter(build_search_q(query, about_fields)).distinct()
        
        for section in about_sections:
            title = section.title_translate if not is_english and section.title_translate else section.title
            description = section.description_translate if not is_english and section.description_translate else section.description
            results.append({
                'title': title or 'About Section',
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/',
                'type': 'About',
                'image': section.image.url if section.image else None
            })
        
        # Search About Aminol
        if is_english:
            about_aminol_fields = ['based_in', 'location', 'exporting_to', 'production_capacity']
        else:
            about_aminol_fields = ['based_in_translate', 'location_translate', 'exporting_to_translate', 
                                 'production_capacity_translate', 'based_in', 'location', 'exporting_to', 'production_capacity']
        
        about_aminol = AboutAminol.objects.filter(build_search_q(query, about_aminol_fields)).distinct()
        
        for about in about_aminol:
            results.append({
                'title': f'About Aminol - Founded {about.founded_year}',
                'description': f'Based in: {about.based_in}, Location: {about.location}',
                'url': '/about/',
                'type': 'About Aminol',
                'image': about.shared_image.url if about.shared_image else None
            })
        
        # Search We Guarantee
        if is_english:
            guarantee_fields = ['title', 'sub_title_one', 'sub_description_one', 'sub_title_two', 
                              'sub_description_two', 'sub_title_three', 'sub_description_three', 
                              'sub_title_four', 'sub_description_four']
        else:
            guarantee_fields = ['title_translate', 'sub_title_one_translate', 'sub_description_one_translate',
                              'sub_title_two_translate', 'sub_description_two_translate', 'sub_title_three_translate',
                              'sub_description_three_translate', 'sub_title_four_translate', 'sub_description_four_translate',
                              'title', 'sub_title_one', 'sub_description_one', 'sub_title_two', 'sub_description_two']
        
        guarantees = WeGuarantee.objects.filter(build_search_q(query, guarantee_fields)).distinct()
        
        for guarantee in guarantees:
            title = guarantee.title_translate if not is_english and guarantee.title_translate else guarantee.title
            results.append({
                'title': title,
                'description': 'We guarantee quality, service, innovation and sustainability',
                'url': '/about/',
                'type': 'Guarantee',
                'image': None
            })
        
        # Search Quality Content
        if is_english:
            quality_fields = ['title', 'description']
        else:
            quality_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        quality_contents = QualityContent.objects.filter(build_search_q(query, quality_fields)).distinct()
        
        for content in quality_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/?tab=quality/',
                'type': 'Quality',
                'image': content.image.url if content.image else None
            })

        # Search Documents & Certifications
        if is_english:
            cert_fields = ['title', 'description']
        else:
            cert_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        certifications_contents = DocumentsCertification.objects.filter(build_search_q(query, cert_fields)).distinct()

        for content in certifications_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/?tab=documents/',
                'type': 'Documents & Certifications',
                'image': content.image.url if content.image else None
            })
        
        # Search Production Content
        if is_english:
            production_fields = ['title', 'description']
        else:
            production_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        production_contents = ProductionContent.objects.filter(build_search_q(query, production_fields)).distinct()
        
        for content in production_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/?tab=production/',
                'type': 'Production',
                'image': content.image.url if content.image else None
            })
        
        # Search Sustainability
        sustainability_items = Sustainability.objects.filter(build_search_q(query, ['main_description', 'main_description_translate'])).distinct()
        
        for item in sustainability_items:
            description = item.main_description_translate if not is_english and item.main_description_translate else item.main_description
            results.append({
                'title': 'Sustainability',
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/?tab=sustainability/',
                'type': 'Sustainability',
                'image': None
            })
        
        # Search Sustainability Content
        if is_english:
            sustainability_fields = ['title', 'description']
        else:
            sustainability_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        sustainability_contents = SustainabilityContent.objects.filter(build_search_q(query, sustainability_fields)).distinct()
        
        for content in sustainability_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/?tab=sustainability/',
                'type': 'Sustainability',
                'image': content.image.url if content.image else None
            })
        
        # Search Contact Info
        if is_english:
            contact_fields = ['title', 'description', 'aminol_headquarters', 'aminol_factory', 
                            'registers', 'contact_address']
        else:
            contact_fields = ['title_translate', 'description_translate', 'aminol_headquarters_translate',
                            'aminol_factory_translate', 'registers_translate', 'contact_address_translate',
                            'title', 'description', 'aminol_headquarters', 'aminol_factory']
        
        contact_infos = ContactInfo.objects.filter(build_search_q(query, contact_fields)).distinct()
        
        for contact in contact_infos:
            title = contact.title_translate if not is_english and contact.title_translate else contact.title
            description = contact.description_translate if not is_english and contact.description_translate else contact.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/contact/',
                'type': 'Contact',
                'image': None
            })
        
        # Search Aminol Official Dealer
        if is_english:
            dealer_fields = ['title', 'title_description', 'description']
        else:
            dealer_fields = ['title_translate', 'title_description_translate', 'description_translate',
                           'title', 'description']
        
        dealer_services = Aminol_Official_Dealer.objects.filter(build_search_q(query, dealer_fields)).distinct()
        
        for service in dealer_services:
            title = service.title_translate if not is_english and service.title_translate else service.title
            description = service.description_translate if not is_english and service.description_translate else service.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/services/dealer/',
                'type': 'Service',
                'image': service.image.url if service.image else None
            })
        
        # Search Aminol Official Dealer Content
        if is_english:
            dealer_content_fields = ['title', 'description']
        else:
            dealer_content_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        dealer_contents = Aminol_Official_Dealer_Content.objects.filter(build_search_q(query, dealer_content_fields)).distinct()
        
        for content in dealer_contents:
            title = content.title_translate if not is_english and content.title_translate else content.title
            description = content.description_translate if not is_english and content.description_translate else content.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/services/dealer/',
                'type': 'Service',
                'image': content.image.url if content.image else None
            })
        
        # Search Laboratory Services
        if is_english:
            lab_fields = ['title', 'description']
        else:
            lab_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        lab_services = Aminol_Labaratory.objects.filter(build_search_q(query, lab_fields)).distinct()
        
        for service in lab_services:
            title = service.title_translate if not is_english and service.title_translate else service.title
            description = service.description_translate if not is_english and service.description_translate else service.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/services/laboratory/',
                'type': 'Laboratory Service',
                'image': service.image.url if service.image else None
            })
        
        # Search Logistics Services
        if is_english:
            logistics_fields = ['title', 'description']
        else:
            logistics_fields = ['title_translate', 'description_translate', 'title', 'description']
        
        logistics_services = Aminol_Logistics.objects.filter(build_search_q(query, logistics_fields)).distinct()
        
        for service in logistics_services:
            title = service.title_translate if not is_english and service.title_translate else service.title
            description = service.description_translate if not is_english and service.description_translate else service.description
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/services/logistics/',
                'type': 'Logistics Service',
                'image': service.image.url if service.image else None
            })
        
        # Remove duplicates based on title and type
        seen = set()
        unique_results = []
        for result in results:
            identifier = (result['title'], result['type'])
            if identifier not in seen:
                seen.add(identifier)
                unique_results.append(result)
        
        results = unique_results
        total_results = len(results)
        
        # Sort results by relevance (exact matches first, then partial matches)
        def calculate_relevance(result):
            title_lower = result['title'].lower()
            desc_lower = result['description'].lower()
            query_lower = query.lower()
            
            # Exact match in title gets highest score
            if query_lower in title_lower:
                return 100
            # Exact match in description gets high score
            elif query_lower in desc_lower:
                return 80
            # Partial word matches get medium score
            else:
                score = 0
                for word in query_lower.split():
                    if word in title_lower:
                        score += 20
                    elif word in desc_lower:
                        score += 10
                return score
        
        results.sort(key=calculate_relevance, reverse=True)
        
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