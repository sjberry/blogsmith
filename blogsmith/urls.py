from django.conf.urls import patterns, url

from blogsmith import views


urlpatterns = patterns('',
    url(r'^/edit/?$', views.ArticleView.as_view(), name='article_add'),
    url(r'^/edit/(?P<slug>[^/]+)/?$', views.ArticleView.as_view(), name='article_edit'),
    url(r'^/render/?$', views.RenderView.as_view(), name='render'),
    url(r'^/?$', 'blogsmith.views.index', name='index'),
)
