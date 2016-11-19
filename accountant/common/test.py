# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve
from django.test import RequestFactory

class RequestFunctionMixin:
    """
    Supplies an easy easy interface to the RequestFactory
    """
    factory = RequestFactory()

    def request(self, method, user=None, url=None, session={}, **kwargs):
        if user == None:
            user = AnonymousUser()
        if url == None:
            url = self.url
        request = method(url)
        request.user = user
        request.session = session
        return self.view(request, url, **kwargs)

    def get_request(self, user=None, url=None, session={}, **kwargs):
        return request(self.request.get, user, url, session, **kwargs)

    def post_request(self, user=None, url=None, session={}, **kwargs):
        return request(self.request.post, user, url, session, **kwargs)


class ViewTestMixin(RequestFunctionMixin):
    """
    Bundles most of the common functionality of view tests

    Uses the Django test client to test for correct template usage, but use
    of RequestFactory is adviced for other tests. To test templates a list
    of the template names should be stored in the 'templates' attribute.
    """
    view = None
    url = None

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_view_uses_correct_templates(self):
        # Check if a non reversed url has been set
        try:
            url = self.explicit_url
        except AttributeError:
            url = self.url

        response = self.client.get(url)

        for t in self.templates:
            with self.subTest(template=t):
                self.assertTemplateUsed(response, t)
