from django.views.generic import DetailView
from tools.models import Tool


class ToolDetailView(DetailView):
    template_name = 'tools/tool_detail.jinja'
    slug_field = 'slug'
    model = Tool
    context_object_name = 'tool'
