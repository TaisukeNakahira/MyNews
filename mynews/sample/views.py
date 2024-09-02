from django.shortcuts import render
from django.views.generic import TemplateView # <-追加する

#---------------------------------------------------------------
#htmlページに表示内容をクラスで作成する。
#---------------------------------------------------------------
class IndexView(TemplateView):
    template_name = "sample/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        op = {
            'テスト1',
            'テスト2',
            'テスト3',
            'テスト4',
            'テスト5',
        }
        context["opinion"] = op
        return context

index = IndexView.as_view()
