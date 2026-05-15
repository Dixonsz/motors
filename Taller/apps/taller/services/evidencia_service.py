from ..models import Evidencia, Recepcion
import cloudinary.uploader

ORDEN_CLOSED_ERROR = "La recepción tiene una orden de servicio cerrada y no se puede modificar."

class EvidenciaService:

    @staticmethod
    def _recepcion_cerrada(recepcion):
        if not recepcion:
            return False
        return recepcion.ordenes_servicio.filter(estado__nombre__iexact="Completado").exists()

    @staticmethod
    def create_evidencia(recepcion_id, tipo=None, url_archivo=None, descripcion=None):
        recepcion = Recepcion.objects.filter(id=recepcion_id).first()
        if recepcion and EvidenciaService._recepcion_cerrada(recepcion):
            raise ValueError(ORDEN_CLOSED_ERROR)
        evidencia = Evidencia.objects.create(
            recepcion_id=recepcion_id,
            tipo=tipo,
            url_archivo=url_archivo,
            descripcion=descripcion
        )
        return evidencia

    @staticmethod
    def create_multiple_evidencias(recepcion_id, archivos, tipo, descripcion=None):

        recepcion = Recepcion.objects.filter(id=recepcion_id).first()
        if recepcion and EvidenciaService._recepcion_cerrada(recepcion):
            raise ValueError(ORDEN_CLOSED_ERROR)

        evidencias = []

        for archivo in archivos:
            evidencia = Evidencia.objects.create(
                recepcion_id=recepcion_id,
                url_archivo=archivo,
                tipo=tipo,  
                descripcion=descripcion
            )
            evidencias.append(evidencia)

        return evidencias


    @staticmethod
    def get_evidencias_by_recepcion(recepcion_id):

        return Evidencia.objects.filter(recepcion_id=recepcion_id)


    @staticmethod
    def get_evidencia_by_id(evidencia_id):

        return Evidencia.objects.filter(id=evidencia_id).first()


    @staticmethod
    def delete_evidencia(evidencia_id):

        evidencia = Evidencia.objects.filter(id=evidencia_id).first()

        if not evidencia:
            raise ValueError("La evidencia no existe")
        if EvidenciaService._recepcion_cerrada(evidencia.recepcion):
            raise ValueError(ORDEN_CLOSED_ERROR)
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

        if EvidenciaService._recepcion_cerrada(evidencia.recepcion):
            raise ValueError(ORDEN_CLOSED_ERROR)

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

