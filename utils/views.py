from django.http import HttpResponse
from django.template import RequestContext, loader
      
def HR(request, template_path, objects, **kwargs):
    template = loader.get_template(template_path)
    context = RequestContext(request, objects)
    return HttpResponse(template.render(context), **kwargs)
