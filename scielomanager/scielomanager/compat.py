from django.shortcuts import render


def render_to_response(template_name, context=None, context_instance=None, **kwargs):
    request = getattr(context_instance, "request", None) if context_instance else None
    if request is None:
        request = kwargs.pop("request", None)
    if request is None:
        raise ValueError("request is required for render_to_response compatibility")
    return render(request, template_name, context or {}, **kwargs)
