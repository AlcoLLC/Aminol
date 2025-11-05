from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from products.models import Product, Product_group, Segments, Oil_Types, Viscosity
from news.models import News
from faq.models import FAQ
from markets.models import Markets_Automotive, Markets_Industrial, Markets_Shipping
from about.models import AboutAminol, Quality, Production, Sustainability, WeGuarantee, DocumentsCertification
from brands.models import Brand_Portal, Brand_Portal_Content
from career.models import Job, Department
from services.models import Aminol_Official_Dealer, Aminol_Labaratory, Aminol_Logistics

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    
    def items(self):
        return [
            'home:home',
            'about:about_page',
            'products:product_list',
            'markets:automotive',
            'markets:industrial',
            'markets:shipping',
            'services:dealer', 
            'services:laboratory', 
            'services:logistics', 
            'contact:contact',
            'career:career',
            'news:news_list',
            'faq:faq'
        ]
    
    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Product.objects.all()
    
    def lastmod(self, obj):
        return obj.created_at
    
    def location(self, obj):
        return reverse('products:product_detail', kwargs={'slug': obj.slug})


class NewsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7
    
    def items(self):
        return News.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.published_date
    
    def location(self, obj):
        return reverse('news:news_detail', kwargs={'slug': obj.slug})


class FAQSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return FAQ.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        # FAQ için spesifik URL pattern bulunamadı, 
        # muhtemelen faq:faq_detail olmalı
        return reverse('faq:faq_detail', kwargs={'id': obj.id})


class MarketsSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        return [
            'markets:automotive',
            'markets:industrial',
            'markets:shipping'
        ]
    
    def location(self, item):
        return reverse(item)


class BrandPortalContentSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    
    def items(self):
        return Brand_Portal_Content.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        # Brand portal content için spesifik detail URL'i brands.urls'de görünmüyor
        # Bu sınıfı kaldırabilir ya da uygun URL pattern ekleyebilirsiniz
        return reverse('brands:brand_portal_content_detail', kwargs={'id': obj.id})


class JobSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.6
    
    def items(self):
        return Job.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        # career:career_steps job_id parametresi kullanıyor
        return reverse('career:career_steps', kwargs={'job_id': obj.id})


class DepartmentSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    
    def items(self):
        return Department.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        # Department için spesifik URL pattern career.urls'de görünmüyor
        # Bu sınıfı kaldırabilirsiniz ya da uygun URL pattern ekleyebilirsiniz
        return reverse('career:department_jobs', kwargs={'slug': obj.slug})


class AboutSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        about_pages = []
        
        # about.urls'de sadece 'about_page' var
        # Diğer sayfalar için URL pattern'ler eklenmeli
        if AboutAminol.objects.exists():
            about_pages.append('about:about_aminol')
            
        if Quality.objects.exists():
            about_pages.append('about:quality')
            
        if Production.objects.exists():
            about_pages.append('about:production')
            
        if Sustainability.objects.exists():
            about_pages.append('about:sustainability')
            
        if WeGuarantee.objects.exists():
            about_pages.append('about:we_guarantee')
            
        if DocumentsCertification.objects.exists():
            about_pages.append('about:documents_certification')
            
        return about_pages
    
    def location(self, item):
        return reverse(item)


class WeGuaranteeSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return WeGuarantee.objects.all()
    
    def location(self, obj):
        return reverse('about:we_guarantee_detail', kwargs={'id': obj.id})


class DocumentsCertificationSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return DocumentsCertification.objects.all()
    
    def location(self, obj):
        return reverse('about:documents_certification_detail', kwargs={'id': obj.id})


class ServicesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        services = []
        
        # Services için sadece ana sayfalar var, detail sayfalar yok
        # Bu sınıfı sadeleştirip ana service sayfalarını döndürebilirsiniz
        services.extend([
            'services:dealer',
            'services:laboratory', 
            'services:logistics'
        ])
            
        return services
    
    def location(self, item):
        return reverse(item)


class AminolOfficialDealerSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Aminol_Official_Dealer.objects.all()
    
    def location(self, obj):
        # services.urls'de detail URL'i yok
        return reverse('services:aminol_official_dealer_detail', kwargs={'id': obj.id})


class AminolLaboratorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Aminol_Labaratory.objects.all()
    
    def location(self, obj):
        # services.urls'de detail URL'i yok
        return reverse('services:aminol_laboratory_detail', kwargs={'id': obj.id})


class AminolLogisticsSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Aminol_Logistics.objects.all()
    
    def location(self, obj):
        # services.urls'de detail URL'i yok
        return reverse('services:aminol_logistics_detail', kwargs={'id': obj.id})


# Mevcut URL pattern'lere göre çalışacak sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'news': NewsSitemap,
    'markets': MarketsSitemap,
    # Aşağıdaki sitemaps için önce URL pattern'ler eklenmeli:
    # 'faq': FAQSitemap,
    # 'brand_portal_content': BrandPortalContentSitemap,
    # 'jobs': JobSitemap,
    # 'departments': DepartmentSitemap,
    # 'about': AboutSitemap,
    # 'we_guarantee': WeGuaranteeSitemap,
    # 'documents_certification': DocumentsCertificationSitemap,
    # 'services': ServicesSitemap,
}