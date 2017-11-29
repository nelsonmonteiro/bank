from django.views.generic import TemplateView


class AutoTemplateView(TemplateView):
    def get_template_names(self):
        return [self.kwargs['template_name']]


