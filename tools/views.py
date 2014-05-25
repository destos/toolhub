from braces.views import LoginRequiredMixin, FormValidMessageMixin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, TemplateView, ListView


from utils.mixins import MPTTUrlMixin
from tools.models import Tool, UserTool
from .forms import CreateUserToolForm, SuggestToolForm


class CreateUserTool(
        LoginRequiredMixin,
        FormValidMessageMixin,
        CreateView):
    """
    Allows user to create a new user tool
    """
    template_name = 'tools/usertool_create.jinja'
    model = UserTool
    form_class = CreateUserToolForm
    form_valid_message = _("Succefully added tool to your library.")

    def get_success_url(self):
        return reverse('account:tool:manager')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(CreateUserTool, self).form_valid(form)


class SuggestTool(
        LoginRequiredMixin,
        FormValidMessageMixin,
        CreateView):
    """
    Allows users to suggest new tool types
    """
    template_name = 'tools/tool_suggest.jinja'
    model = Tool
    form_class = SuggestToolForm
    form_valid_message = _("""
        Thanks for suggesting a new tool type! We'll take it from here!""")

    def get_success_url(self):
        return reverse('account:tool:manager')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        assert self.object.published is False
        return super(SuggestTool, self).form_valid(form)


class ToolList(
        MPTTUrlMixin,
        ListView):
    """
    A filterable list of tools
    """
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


class ToolDetailView(
        MPTTUrlMixin,
        TemplateView):
    template_name = 'tools/tool_detail.jinja'
    mptt_context_object_name = 'tool'

    def get_object(self):
        if self.mptt_object:
            return self.mptt_object
        else:
            return super(ToolDetailView, self).get_object()
