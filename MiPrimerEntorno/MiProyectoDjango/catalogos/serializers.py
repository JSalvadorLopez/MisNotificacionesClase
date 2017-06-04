from rest_framework import serializers
from .models import Categoria

class CategoriaSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only=True)
	categoria = serializers.CharField()
	descripcion = serializers.CharField()

	def create(self, validated_data):
		return Categoria.objects.create(**validated_data)

	def update (self, instance, validated_data):
		instance.categoria = validated_data.get('categoria', instance.categoria)
		instance.descripcion = validated_data.get('descripcion', instance.descripcion)
		instance.save()
		return instance


class CategoriaModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categoria
		fields = ('id','categoria','descripcion')