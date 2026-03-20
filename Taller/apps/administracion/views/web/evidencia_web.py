from django.shortcuts import render, redirect, get_object_or_404
from ...models import Recepcion
from ...services.evidencia_service import EvidenciaService
from ...services.recepcion_service import RecepcionService


def evidencia_lista(request, recepcion_id):

    recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
    evidencias = EvidenciaService.get_evidencias_by_recepcion(recepcion_id)

    return render(
        request,
        'evidencias/evidencias_lista.html',
        {
            'recepcion': recepcion,
            'evidencias': evidencias
        }
    )


def evidencia_create(request, recepcion_id):
    recepcion = get_object_or_404(Recepcion, id=recepcion_id)

    if request.method == 'POST':
        url_archivo = request.FILES.get('url_archivo')
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo', 'imagen')

        EvidenciaService.create_evidencia(
            recepcion_id=recepcion.id,
            tipo=tipo,
            url_archivo=url_archivo,
            descripcion=descripcion
        )
        return redirect('recepcion_lista')

    return render(request, 'evidencias/evidencias_crear.html', {'recepcion': recepcion})


def evidencia_editar(request, evidencia_id):

    evidencias = EvidenciaService.get_evidencia_by_id(evidencia_id)

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')
        url_archivo = request.FILES.get('url_archivo')

        EvidenciaService.update_evidencia(
            evidencia_id,
            tipo=tipo,
            url_archivo=url_archivo,
            descripcion=descripcion
        )

        return redirect('evidencia_lista', recepcion_id=evidencias.recepcion.id)

    return render(request, 'evidencias/evidencias_editar.html', {'evidencia': evidencias})


def evidencia_eliminar(request, evidencia_id):

    evidencia = EvidenciaService.get_evidencia_by_id(evidencia_id)

    if request.method == 'POST':

        recepcion_id = evidencia.recepcion.id
        EvidenciaService.delete_evidencia(evidencia_id)

        return redirect('evidencia_lista', recepcion_id=recepcion_id)

    return render(
        request,
        'evidencias/evidencias_eliminar.html',
        {
            'evidencia': evidencia
        }
    )

def recepcion_detalle(request, recepcion_id):

    recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
    evidencias = EvidenciaService.get_evidencias_by_recepcion(recepcion_id)

    return render(
        request,
        'recepciones/recepcion_detalle.html',
        {
            'recepcion': recepcion,
            'evidencias': evidencias
        }
    )