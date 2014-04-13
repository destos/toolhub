from django.views.generic import DetailView, ListView
from tools.models import Tool


# abstract the object retrieval?
class MPTTUrlMixin(object):
    mptt_context_object_name = 'mptt_object'

    def dispatch(self, request, *args, **kwargs):
        """get passed in mptt_urls object which is the leaf node"""
        self.mptt_object = kwargs.pop('mptt_urls', {}).get('object', None)
        return super(MPTTUrlMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self):
        context = super(MPTTUrlMixin, self).get_context_data()
        context[self.mptt_context_object_name] = self.mptt_object
        return context


class ToolList(MPTTUrlMixin, ListView):
    template_name = 'tools/tool_list.jinja'
    queryset = Tool.objects.published()
    context_object_name = 'tool_list'
    mptt_context_object_name = 'tool_class'
    paginate_by = 30

    def get_queryset(self):
        qs = super(ToolList, self).get_queryset()
        if self.mptt_object:
            #TODO: show all tools that are inside a category and it's decendants
            return qs.children_tools(self.mptt_object)
        else:
            return qs


class ToolDetailView(DetailView):
    template_name = 'tools/tool_detail.jinja'
    slug_field = 'slug'
    model = Tool
    context_object_name = 'tool'
