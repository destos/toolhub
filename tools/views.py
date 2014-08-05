from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView


# from toolhub.mixins import MPTTUrlMixin
from tools.models import Tool, ToolClassification, UserTool
from .forms import CreateUserToolForm, SuggestToolForm
from toolhub.mixins import LoginRequiredMixin, FormValidMessageMixin


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


class BaseToolList(ListView):
    template_name = 'tools/tool_list.jinja'
    queryset = Tool.objects.published()
    context_object_name = 'tool_list'
    paginate_by = 6


class ToolList(BaseToolList):
    """
    A filterable list of tools by classification
    """
    tool_class = None

    def dispatch(self, request, *args, **kwargs):
        tool_class_slug = kwargs.pop('tool_class_slug', None)
        if tool_class_slug:
            self.tool_class = get_object_or_404(
                ToolClassification, slug=tool_class_slug)

        return super(ToolList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, object=None):
        context = super(ToolList, self).get_context_data()
        context['tool_class'] = self.tool_class
        return context

    def get_queryset(self):
        qs = super(ToolList, self).get_queryset()
        if self.tool_class:
            #TODO: show all tools that are inside a category and it's decendants
            return qs.children_tools(self.tool_class)
        else:
            return qs


class ToolDetailView(DetailView):
    template_name = 'tools/tool_detail.jinja'
    model = Tool
    slug_url_kwarg = 'tool_slug'
    context_object_name = 'tool'
