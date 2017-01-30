# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.urls.exceptions import NoReverseMatch
from rest_framework import routers
from rest_framework import views
from rest_framework import reverse
from rest_framework import response

# Taken from http://stackoverflow.com/questions/18817988/using-django-rest-frameworks-browsable-api-with-apiviews#23321478
class HybridRouter(routers.DefaultRouter): # pragma: no cover
    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self._api_view_urls = {}

    def add_api_view(self, name, url):
        self._api_view_urls[name] = url

    def remove_api_view(self, name):
        del self._api_view_urls[name]

    @property
    def api_view_urls(self):
        ret = {}
        ret.update(self._api_view_urls)
        return ret

    def get_urls(self):
        urls = super(HybridRouter, self).get_urls()
        for api_view_key in self._api_view_urls.keys():
            urls.append(self._api_view_urls[api_view_key])
        return urls

    def get_api_root_view(self, api_urls=None):
        # Copy the following block from Default Router
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        view_renderers = list(self.root_renderers)
        schema_media_types = []

        if api_urls and self.schema_title:
            view_renderers += list(self.schema_renderers)
            schema_generator = SchemaGenerator(title=self.schema_title,
                url=self.schema_url, patterns=api_urls)
            schema_media_types = [renderer.media_type
                for renderer in self.schema_renderers]

        api_view_urls = self._api_view_urls

        class APIRoot(views.APIView):
            _ignore_model_permissions = True
            renderer_classes = view_renderers

            def get(self, request, *args, **kwargs):
                if request.accepted_renderer.media_type in schema_media_types:
                    # Return a schema response.
                    schema = schema_generator.get_schema(request)
                    if schema is None:
                        raise exceptions.PermissionDenied()
                    return Response(schema)

                # Return a plain {"name": "hyperlink"} response.
                ret = OrderedDict()
                namespace = request.resolver_match.namespace
                for key, url_name in api_root_dict.items():
                    if namespace:
                        url_name = namespace + ':' + url_name
                    try:
                        ret[key] = reverse.reverse(url_name, args=args,
                            kwargs=kwargs, request=request,
                            format=kwargs.get('format', None))
                    except NoReverseMatch:
                        # Don't bail out if eg. no list routes exist, only
                        # detail routes.
                        continue

                # In addition to what had been added, now add the APIView urls
                for api_view_key in api_view_urls.keys():
                    url_name = api_view_urls[api_view_key].name
                    if namespace:
                        url_name = namespace + ':' + url_name
                    ret[api_view_key] = reverse.reverse(url_name,
                        request=request, format=kwargs.get('format'))

                return response.Response(ret)

        return APIRoot.as_view()
