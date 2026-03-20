import re
from datetime import timedelta

from django.utils.dateparse import parse_duration

from ..models import Servicio
from ..models.categoria_servicio import CategoriaServicio
from django.core.exceptions import ObjectDoesNotExist

class ServicioService:

    @staticmethod
    def _get_categoria_or_error(categoria_id):
        try:
            return CategoriaServicio.objects.get(id=categoria_id)
        except ObjectDoesNotExist:
            raise ValueError("La categoria del servicio no existe.")

    @staticmethod
    def _parse_duracion_estimada(duracion_estimada):
        if duracion_estimada is None or duracion_estimada == "":
            return None

        if isinstance(duracion_estimada, timedelta):
            return duracion_estimada

        if isinstance(duracion_estimada, str):
            valor = duracion_estimada.strip()

            # Acepta formato HH:MM desde formularios web.
            if re.fullmatch(r"\d{1,2}:\d{2}", valor):
                horas, minutos = map(int, valor.split(":"))
                if minutos >= 60:
                    raise ValueError("La duración debe estar en formato HH:MM válido.")
                return timedelta(hours=horas, minutes=minutos)

            parsed = parse_duration(valor)
            if parsed is not None:
                return parsed

        raise ValueError("La duración debe estar en formato HH:MM.")

    @staticmethod
    def get_all_servicios():
        return Servicio.objects.all()
    
    @staticmethod
    def get_servicio_by_id(servicio_id):
        try:
            return Servicio.objects.get(id=servicio_id)
        except ObjectDoesNotExist:
            return None
        
    @staticmethod
    def create_servicio(nombre, categoria_id, descripcion, precio_base, duracion_estimada, is_active=True):

        if Servicio.objects.filter(nombre=nombre).exists():
            raise ValueError("El nombre del servicio ya existe.")
        
        categoria_servicio = ServicioService._get_categoria_or_error(categoria_id)
        duracion_estimada = ServicioService._parse_duracion_estimada(duracion_estimada)
        servicio = Servicio(
            nombre=nombre,
            categoria_servicio=categoria_servicio,
            descripcion=descripcion,
            precio_base=precio_base,
            duracion_estimada=duracion_estimada,
            is_active=is_active
        )  
        servicio.save()
        return servicio
        

        

    @staticmethod
    def update_servicio(servicio_id, categoria_id=None, nombre=None, descripcion=None, precio_base=None, duracion_estimada=None, is_active=None):
        servicio = ServicioService.get_servicio_by_id(servicio_id)
        if not servicio:
            raise ValueError("El servicio no existe.")

        if categoria_id:
            categoria = ServicioService._get_categoria_or_error(categoria_id)
            servicio.categoria_servicio = categoria
        if nombre:
            servicio.nombre = nombre
        if descripcion:
            servicio.descripcion = descripcion
        if precio_base is not None:
            servicio.precio_base = precio_base
        if duracion_estimada is not None:
            servicio.duracion_estimada = ServicioService._parse_duracion_estimada(duracion_estimada)
        if is_active is not None:
            servicio.is_active = is_active

        servicio.save()
        return servicio

    @staticmethod
    def delete_servicio(servicio_id):
        servicio = ServicioService.get_servicio_by_id(servicio_id)
        if not servicio:
            raise ValueError("El servicio no existe.")
        servicio.delete()
      