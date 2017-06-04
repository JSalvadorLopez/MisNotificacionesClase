from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Categoria, Producto
from django.template import loader
from .forms import ProductoForm
from django.views.generic import ListView

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import CategoriaSerializer, CategoriaModelSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.views import APIView

#mensajeria push
from fcm.utils import get_device_model
Device = get_device_model()



def index(request):
	return render(request,"index.html")


class indexView():
	template_name="index.html"

# Create your views here.
def mensajeria(request):

		

	if	request.method == 'POST':
		dvs=[]
		for k in request.POST.keys():
			print(k)
			if k.isdigit():
				dvs.append(int(k))

		print(dvs)
		devices=Device.objects.filter(dev_id__in=dvs)
		print(devices)
		r=devices.send_message(request.POST['mensaje'])
		print(r)
		return HttpResponse(r)	

	else:
		devices = Device.objects.all()
		#print(devices[0].reg_id)
		context = {'devices' : devices}
		template = loader.get_template('mensajeria.html')
		return HttpResponse(template.render(context,request))	



def hello_world(request):
	return render(request,"index.html")

def hello_template(request):
	return render(request,"index.html")

def obtener_categorias(request):
	c = Categoria(categoria = "Carnes frias", descripcion = "Todo tipo de embutido")
	c.save()
	categorias = Categoria.objects.order_by('categoria')
	context = {'categorias' : categorias}
	return render(request,'categorias.html', context)

def listado_productos(request):
	p = Producto.objects.order_by('id')
	template = loader.get_template('productos_list.html')
	context = {'productos' : p}
	return HttpResponse(template.render(context,request))

def product_detail(request, pk):
	product = get_object_or_404(Producto, pk=pk)
	template = loader.get_template('producto_detail.html')
	context = {
		'product': product
	}
	return HttpResponse(template.render(context,request))

def nuevo_producto(request):
	if request.method == 'POST':
		form = ProductoForm(request.POST,request.FILES)

		if form.is_valid():
			product = form.save()
			product.save()
			return HttpResponseRedirect('/catalogos/producto/')
	else:
		form = ProductoForm()

	template = loader.get_template('nuevo_producto.html')
	
	context = {
		'form':form

	}
	return HttpResponse(template.render(context,request))

class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'aplication/json'
		super(JSONResponse,self).__init__(content, **kwargs)

@csrf_exempt
def categoria_list(request):
	if request.method == 'GET':
		categorias =  Categoria.get_objects.all()
		serializer = CategoriaModelSerializer(categorias, many=True)
		#return JSONResponse(serializer.data)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CategoriaModelSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errora, status=400)

@api_view(['GET', 'POST'])
def categoria_list_api(request, format=None):
	if request.method == 'GET':
		categorias =  Categoria.objects.all()
		serializer = CategoriaModelSerializer(categorias, many=True)
		#return JSONResponse(serializer.data)
		#return JsonResponse(serializer.data, safe=False)
		return Response(serializer.data)

	elif request.method == 'POST':
		#data = JSONParser().parse(request)
		serializer = CategoriaModelSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			#return JSONResponse(serializer.data, status=201)
			return Response(serializer.data, status=status.HTTP_201_CREATED) 
		#return JSONResponse(serializer.errors, status=400)
		return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def categoria_detail(request, pk):
	"""
	Retrieve, update or delete a serie.
	"""
	try:
		categoria = Categoria.objects.get(pk=pk)
	except Categoria.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = CategoriaModelSerializer(categoria)
		#return JSONResponse(serializer.data)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CategoriaModelSerializer(categoria, data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		categoria.delete()
		return HttpResponse(status=204)

@api_view(['GET','PUT','DELETE'])
def categoria_detail_api(request, pk, format=None):
	"""
	Retrieve, update or delete a serie.
	"""
	try:
		categoria = Categoria.objects.get(pk=pk)
	except Categoria.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = CategoriaModelSerializer(categoria)
		#return JSONResponse(serializer.data)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		#data = JSONParser().parse(request)
		serializer = CategoriaModelSerializer(categoria, data=request.data)
		if serializer.is_valid():
			serializer.save()
			#return JSONResponse(serializer.data)
			return Response(serializer.data)
		#return JSONResponse(serializer.errors, status=400)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		categoria.delete()
		#return HttpResponse(status=204)
		return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriaListClassView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Categoria.objects.all()
        serializer = CategoriaModelSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategoriaModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriaDetailClassView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        categoria = self.get_object(pk)
        serializer = CategoriaModelSerializer(categoria)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        categoria = self.get_object(pk)
        serializer = CategoriaModelSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        categoria = self.get_object(pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)