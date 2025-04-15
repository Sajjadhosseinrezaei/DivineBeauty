from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme

def redirect_with_next(request, default='/', param_name='next'):
    """
    Redirects user to a safe 'next' URL if available, otherwise to default.

    Args:
        request: The current HttpRequest object.
        default: The fallback URL to redirect if next is invalid or missing.
        param_name: The GET or POST param to check for next URL (default is 'next').

    Returns:
        HttpResponseRedirect
    """
    next_url = request.GET.get(param_name) or request.POST.get(param_name)
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect(default)
