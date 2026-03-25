import csv
from datetime import datetime, timedelta

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from ...services.reportes_service import ReportesService


def reporte_clientes(request):
    fecha_inicio, fecha_fin = _obtener_rango_fechas(request)
    reporte = ReportesService.generar_reporte_clientes(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    if request.GET.get('formato') == 'csv':
        return _exportar_clientes_csv(reporte['filas'], fecha_inicio, fecha_fin)

    context = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'filas': reporte['filas'],
        'resumen': reporte['resumen'],
    }
    return render(request, 'reportes/clientes_reporte.html', context)


def _obtener_rango_fechas(request):
    hoy = timezone.localdate()
    hace_30_dias = hoy - timedelta(days=30)

    fecha_inicio_txt = request.GET.get('fecha_inicio')
    fecha_fin_txt = request.GET.get('fecha_fin')

    fecha_inicio = hace_30_dias
    fecha_fin = hoy

    if fecha_inicio_txt:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_txt, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'La fecha de inicio no es valida. Se aplico el valor por defecto (ultimos 30 dias).')

    if fecha_fin_txt:
        try:
            fecha_fin = datetime.strptime(fecha_fin_txt, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'La fecha fin no es valida. Se aplico el valor por defecto (hoy).')

    if fecha_inicio > fecha_fin:
        messages.error(request, 'La fecha de inicio no puede ser mayor que la fecha fin. Se ajusto automaticamente el rango.')
        fecha_inicio, fecha_fin = fecha_fin, fecha_inicio

    return fecha_inicio, fecha_fin


def _exportar_clientes_csv(filas, fecha_inicio, fecha_fin):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename="reporte_clientes_{fecha_inicio}_{fecha_fin}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        'ID',
        'Nombre',
        'Correo',
        'Telefono',
        'Cedula',
        'Direccion',
        'Vehiculos',
        'Citas',
        'Recepciones',
        'Ordenes',
        'Facturado',
    ])

    for fila in filas:
        writer.writerow([
            fila['id'],
            fila['nombre'],
            fila['correo'],
            fila['telefono'],
            fila['cedula'],
            fila['direccion'],
            fila['vehiculos'],
            fila['citas'],
            fila['recepciones'],
            fila['ordenes'],
            f"{fila['facturado']:.2f}",
        ])

    return response

