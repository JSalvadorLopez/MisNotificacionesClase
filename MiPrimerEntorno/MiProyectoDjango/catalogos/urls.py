from django.conf.urls import url
from . import views

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^autenticacion/$', views.hello_world, name="hello"),
    url(r'^$', views.mensajeria, name="mensajes"),
    url(r'^template/', views.hello_template, name="template"),
    url(r'^categorias/', views.obtener_categorias, name="ctgrs"),
    url(r'^producto/$', views.listado_productos, name="listado"),
    url(r'^producto/(?P<pk>[0-9]+)/$', views.product_detail, name="detalle"),
    url(r'^producto/new', views.nuevo_producto, name="nuevo_producto"),
    url(r'^categoriaAPI/$', views.categoria_list,name='apicats'),
    url(r'^categoriaAPI/(?P<pk>[0-9]+)/$', views.categoria_detail,name='apicatsby'),
] + format_suffix_patterns(
			[url(r'^categoriaapiview/$', views.categoria_list_api),
    		url(r'^categoriaapiview/(?P<pk>[0-9]+)/$', views.categoria_detail_api),
            url(r'^categoriaclassview/$', views.CategoriaListClassView.as_view()),
            url(r'^categoriaclassview/(?P<pk>[0-9]+)/$', views.CategoriaDetailClassView.as_view()),
    		]
    ) 
