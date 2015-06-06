from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from blogsmith.forms import ArticleForm
from blogsmith.models import Article
from blogsmith.permissions import AuthenticationMixin, permission
from blogsmith.renderers import MarkdownRenderer


class ArticleView(AuthenticationMixin, View):
    def get_base_context(self, request, slug=None):
        args = []
        kwargs = {}

        if slug:
            article = get_object_or_404(Article, slug__exact=slug)
            title = 'Edit Article'
            form_url = reverse('article_edit', kwargs={'slug': slug})
            kwargs['instance'] = article
            kwargs['initial'] = {
                'content': article.source.read(),
                'slug': article.slug,
                'tags': article.text_tags
            }
        else:
            title = 'Add Article'
            form_url = reverse('article_add')

        if request.method == 'POST':
            args.append(request.POST)

        context = {
            'title': title,
            'form_url': form_url
        }

        if slug or request.method == 'POST':
            context['form'] = ArticleForm(*args, **kwargs)

        return context

    def get(self, request, slug=None):
        context = self.get_base_context(request, slug)

        return render(request, 'blogsmith/edit.html', context)

    def post(self, request, slug=None):
        context = self.get_base_context(request, slug)
        form = context['form']

        form.full_clean()

        print(form.cleaned_data)

        if not form.is_valid():
            return render(request, 'blogsmith/edit.html', context)

        tags = form.cleaned_data.get('tags')
        content = form.cleaned_data.get('content')

        form.save(commit=False)
        form.instance.publish(content, tags)

        return redirect(reverse('index'))


# $.ajax('/blogsmith/render', { method: 'POST', contentType: 'text/plain', data: '#title\nhello' }).done(function() { console.log(arguments); })
class RenderView(AuthenticationMixin, View):
    def post(self, request):
        markdown = request.body
        html = MarkdownRenderer().render(markdown)

        return HttpResponse(html)


@permission
def index(request):
    return render(request, 'blogsmith/index.html', {
        'title': 'Blogsmith'
    })
