from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from ...models import Recepcion
from ...services.evidencia_service import EvidenciaService
from ...services.recepcion_service import RecepcionService
from config.security import access_required

ORDEN_CLOSED_ERROR = "La recepción tiene una orden de servicio cerrada y no se puede modificar."

@access_required("Recepciones", "ver")
def evidencia_lista(request, recepcion_id):

    recepcion = RecepcionService.get_recepcion_by_id(recepcion_id)
    evidencias = EvidenciaService.get_evidencias_by_recepcion(recepcion_id)
    paginator = Paginator(evidencias, 10)
    page_number = request.GET.get('page')
    evidencias = paginator.get_page(page_number)
    bloqueada = RecepcionService.is_recepcion_cerrada(recepcion)

    return render(
        request,
        'evidencias/evidencias_lista.html',
        {
            'recepcion': recepcion,
            'evidencias': evidencias,
            'bloqueada': bloqueada
        }
    )

@access_required("Recepciones", "crear")
def evidencia_create(request, recepcion_id):
    recepcion = get_object_or_404(Recepcion, id=recepcion_id)

    if RecepcionService.is_recepcion_cerrada(recepcion):
        messages.error(request, ORDEN_CLOSED_ERROR)
        return redirect('recepciones_detalle', recepcion_id=recepcion.id)

    if request.method == 'POST':
        archivos = request.FILES.getlist('url_archivo') 
        descripcion = request.POST.get('descripcion', '')
        tipo = request.POST.get('tipo', 'foto')

        if not archivos:
            messages.error(request, 'Debes seleccionar al menos una foto.')
            return render(request, 'evidencias/evidencias_crear.html', {'recepcion': recepcion})

        try:
            EvidenciaService.create_multiple_evidencias(
                recepcion_id=recepcion.id,
                archivos=archivos,
                tipo=tipo,
                descripcion=descripcion  # ← agregar descripción al método
            )
            messages.success(request, f'{len(archivos)} evidencia(s) subida(s) correctamente.')
        except Exception as exc:
            messages.error(request, str(exc))

        return redirect('evidencia_lista', recepcion_id=recepcion.id)

    return render(request, 'evidencias/evidencias_crear.html', {'recepcion': recepcion})


@access_required("Recepciones", "editar")
def evidencia_editar(request, evidencia_id):

    evidencias = EvidenciaService.get_evidencia_by_id(evidencia_id)
    if not evidencias:
        messages.error(request, 'La evidencia no existe.')
        return redirect('recepciones_lista')

    if RecepcionService.is_recepcion_cerrada(evidencias.recepcion):
        messages.error(request, ORDEN_CLOSED_ERROR)
        return redirect('evidencia_lista', recepcion_id=evidencias.recepcion.id)

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')
        url_archivo = request.FILES.get('url_archivo')

        try:
            EvidenciaService.update_evidencia(
                evidencia_id,
                tipo=tipo,
                url_archivo=url_archivo,
                descripcion=descripcion
            )
            messages.success(request, 'Evidencia actualizada correctamente.')
        except ValueError as exc:
            messages.error(request, str(exc))
            return render(request, 'evidencias/evidencias_editar.html', {'evidencia': evidencias})

        return redirect('evidencia_lista', recepcion_id=evidencias.recepcion.id)

    return render(request, 'evidencias/evidencias_editar.html', {'evidencia': evidencias})


@access_required("Recepciones", "eliminar")
def evidencia_eliminar(request, evidencia_id):

    evidencia = EvidenciaService.get_evidencia_by_id(evidencia_id)
    if not evidencia:
        messages.error(request, 'La evidencia no existe.')
        return redirect('recepciones_lista')

    if RecepcionService.is_recepcion_cerrada(evidencia.recepcion):
        messages.error(request, ORDEN_CLOSED_ERROR)
        return redirect('evidencia_lista', recepcion_id=evidencia.recepcion.id)

    if request.method == 'POST':

        recepcion_id = evidencia.recepcion.id
        try:
            EvidenciaService.delete_evidencia(evidencia_id)
            messages.success(request, 'Evidencia eliminada correctamente.')
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect('evidencia_lista', recepcion_id=recepcion_id)

        return redirect('evidencia_lista', recepcion_id=recepcion_id)

    return render(
        request,
        'evidencias/evidencias_eliminar.html',
        {
            'evidencia': evidencia
        }
    )

def evidencia_detalle(request, recepcion_id):

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
