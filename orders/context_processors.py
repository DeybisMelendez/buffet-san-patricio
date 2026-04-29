from core.config import BUSINESS_INFO


def company_info(request):
    """Provee información del negocio a todas las plantillas."""
    return {"company": BUSINESS_INFO}
