from django.core.validators import URLValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.views.generic.list import ListView
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from shortener.models import Url

from .utils import generate_subpart_inner, LoggingResponse


class IndexView(ListView):
    '''Main page view with user's redirect history pagination'''
    template_name = 'shortener/index.html'
    context_object_name = 'urls'
    model = Url
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        queryset = super(IndexView, self).get_queryset()
        session_key = self.request.session.session_key
        # Don't hit db if user is new
        if session_key:
            return queryset.filter(
                session_key=session_key).order_by('-created_at')
        return queryset.none()


def shorten_view(request):
    '''
    Creates a new Url model object with shortened link
    and returns new URL as json response back
    '''
    if request.method == 'POST':
        # Link to be shorten
        url = request.POST.get('url')
        # Subpart desired by user (optional)
        subpart_request = request.POST.get('custom_subpart')
        # If subpart is not provided, it will be generated
        subpart_inner = subpart_request or generate_subpart_inner()
        # Ensure the session is exist
        if not request.session.session_key:
            request.session.save()
        session = request.session.session_key

        if url:
            # Сheck if the provided link is valid
            try:
                validate_url = URLValidator(schemes=('http', 'https'))
                validate_url(url)
            except ValidationError:
                return LoggingResponse(
                    {'error':
                     'Error! URL you entered is incorrect.'},
                    'ERROR 422 %s > %s BY %s' %
                    (url, subpart_inner, session),
                    status=422)

            # Provided subpart validation
            if subpart_request:
                # Сheck if subpart matches pattern
                try:
                    validate_subpart = RegexValidator(r'^[\w0-9]{6}$')
                    validate_subpart(subpart_inner)
                except ValidationError:
                    return LoggingResponse(
                        {'error': 'Error! Subpart must be a six-letter word.'},
                        'ERROR 422 %s > %s BY %s' %
                        (url, subpart_inner, session),
                        status=422)

                # Subpart must be unique
                if Url.objects.filter(subpart_inner=subpart_inner).exists():
                    return LoggingResponse(
                        {'error': 'Error! This subpart already exists.'},
                        'ERROR 409 %s > %s BY %s' %
                        (url, subpart_inner, session),
                        status=409)

            # Create Url object, associated with anonimous user
            new_url = Url(subpart_inner=subpart_inner,
                          subpart_outer=url,
                          session_key=session)
            new_url.save()

            # Cache redirect url for later use
            cache.set(subpart_inner, url, timeout=settings.CACHE_TTL)

            # Return new short URL
            context = {
                'subpart_inner': '%s/%s' % (request.META['HTTP_HOST'],
                                            subpart_inner)}

            return LoggingResponse(
                context, 'SHORTEN %s > %s BY %s' %
                (url, subpart_inner, session))

        return LoggingResponse(
            {'error': 'Error! You did not enter an URL.'},
            'ERROR 400 %s > %s BY %s' %
            (url, subpart_inner, session),
            status=400)

    return LoggingResponse(
        {'error': 'Wrong method.'},
        'ERROR 405 %s > %s BY %s METHOD %s' %
        (url, subpart_inner, session, request.method),
        status=405)


def redirect_view(request, subpart_inner):
    '''Redirect to an external URL from shortened before'''
    # Resolve the subpart into a Url model object
    if subpart_inner in cache:
        # Get url from cache
        url = cache.get(subpart_inner)
    else:
        # Get redirect url from db
        url = get_object_or_404(Url, pk=subpart_inner)
        # Cache redirect url for later use
        cache.set(subpart_inner, url.subpart_outer, timeout=settings.CACHE_TTL)
    return HttpResponseRedirect(url)
