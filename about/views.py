from django.shortcuts import render
from .models import (
    AboutAminol, Quality, WeGuarantee, Production,
    DocumentsCertification, Sustainability
)
from home.models import PartnerLogo, CarLogo, Gallery as GalleryImage

def about_page_view(request):
    about_aminol = AboutAminol.objects.last()

    about_sections = []
    if about_aminol:
        about_sections = about_aminol.sections.all()

    quality = Quality.objects.last()

    quality_contents = []
    if quality:
        quality_contents = quality.contents.all()

    guarantee = WeGuarantee.objects.last()
    production = Production.objects.last()

    production_contents = []
    if production:
        production_contents = production.contents.all()

    documents_cert = DocumentsCertification.objects.last()

    sustainability = Sustainability.objects.last()

    sustainability_contents = []
    if sustainability:
        sustainability_contents = sustainability.contents.all()

    partner_logos = PartnerLogo.objects.all()
    car_logos = CarLogo.objects.all()
    images = GalleryImage.objects.all().order_by('-created_at')

    context = {
        'about_aminol': about_aminol,
        'about_sections': about_sections,
        'quality': quality,
        'quality_contents': quality_contents,
        'guarantee': guarantee,
        'production': production,
        'production_contents': production_contents,
        'documents_cert': documents_cert,
        'sustainability': sustainability,
        'sustainability_contents': sustainability_contents,
        'partner_logos': partner_logos,
        'car_logos': car_logos,
        'images': images,

    }


    return render(request, 'about.html', context)
