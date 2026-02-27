from .models import Company


def company_info(request):
    """Provee información de la empresa a todas las plantillas."""
    company = Company.objects.first()
    return {"company": company}
