from ..models import Evidencia, Recepcion
import cloudinary.uploader

class EvidenciaService:

    @staticmethod
    def create_evidencia(recepcion_id, tipo=None, url_archivo=None, descripcion=None):
        evidencia = Evidencia.objects.create(
            recepcion_id=recepcion_id,
            tipo=tipo,
            url_archivo=url_archivo,
            descripcion=descripcion
        )
        return evidencia

    @staticmethod
    def create_multiple_evidencias(recepcion_id, archivos, tipo):

        evidencias = []

        for archivo in archivos:
            evidencia = Evidencia.objects.create(
                recepcion_id=recepcion_id,
                url_archivo=archivo,
                tipo=tipo
            )
            evidencias.append(evidencia)

        return evidencias


    @staticmethod
    def get_evidencias_by_recepcion(recepcion_id):

        return Evidencia.objects.filter(recepcion_id=recepcion_id)


    @staticmethod
    def delete_evidencia(evidencia_id):

        evidencia = Evidencia.objects.filter(id=evidencia_id).first()

        if not evidencia:
            raise ValueError("La evidencia no existe")
        if evidencia.url_archivo:
            resource_type = "image"

            if evidencia.tipo == 'video':
                resource_type = "video"
            
            cloudinary.uploader.destroy(
                evidencia.url_archivo.public_id,
                resource_type = resource_type
            )
        evidencia.delete()

      
    @staticmethod
    def update_evidencia(evidencia_id, tipo=None, url_archivo=None, descripcion=None):
        evidencia = Evidencia.objects.filter(id=evidencia_id).first()

        if not evidencia:
            raise ValueError("La evidencia no existe")

        if url_archivo:
            resource_type = "image"
            if evidencia.tipo == "video":
                resource_type = "video"

            if evidencia.url_archivo:
                cloudinary.uploader.destroy(
                    evidencia.url_archivo.public_id,
                    resource_type=resource_type
                )

            evidencia.url_archivo = url_archivo

        if tipo:
            evidencia.tipo = tipo

        if descripcion:
            evidencia.descripcion = descripcion

        evidencia.save()
        return evidencia

