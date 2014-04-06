from django.views.generic import DetailView, ListView
from tools.models import Tool


class ToolList(ListView):
    template_name = 'tools/tool_list.jinja'
    queryset = Tool.objects.published()


class ToolDetailView(DetailView):
    template_name = 'tools/tool_detail.jinja'
    slug_field = 'slug'
    model = Tool
    context_object_name = 'tool'
