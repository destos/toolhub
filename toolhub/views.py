# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, View
from django.template import loader, RequestContext
from django import http


class Homepage(TemplateView):
    template_name = "toolhub/home.jinja"


class GenericView(View):
    response_class = http.HttpResponse
    content_type = "text/html"
    template_name = None

    def get_context_data(self):
        return {"view": self}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        output = loader.render_to_string(
            self.template_name, context, context_instance=RequestContext(request))
        return self.response_class(output, content_type=self.content_type)


class ErrorView(GenericView):
    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class PageNotFound(ErrorView):
    template_name = "404.jinja"
    response_class = http.HttpResponseNotFound


class PermissionDenied(ErrorView):
    template_name = "403.jinja"
    response_class = http.HttpResponseForbidden


class BadRequest(ErrorView):
    template_name = "400.jinja"
    response_class = http.HttpResponseBadRequest


class ServerError(ErrorView):
    template_name = "500.jinja"
    response_class = http.HttpResponseServerError
