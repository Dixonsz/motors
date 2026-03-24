from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from ...services.agenda_horario_service import AgendaHorarioService


def _es_bloqueo_todo_dia(agenda_horario):
    return (
        agenda_horario.tipo_bloque == 'bloqueado'
        and str(agenda_horario.hora_inicio) in ('00:00', '00:00:00')
        and str(agenda_horario.hora_fin) in ('23:59', '23:59:00')
    )


def agenda_horario_lista(request):
    agenda_horarios = AgendaHorarioService.get_all_agenda_horarios()
    paginator = Paginator(agenda_horarios, 10)
    page_number = request.GET.get('page')
    agenda_horarios = paginator.get_page(page_number)

    return render(request, 'agenda_horarios/agenda_horarios_lista.html', {'agenda_horarios': agenda_horarios})

def agenda_horario_create(request):
    dias_semana_choices = AgendaHorarioService.get_dias_semana_choices()
    tipos_bloque_choices = AgendaHorarioService.get_tipos_bloque_choices()

    if request.method == 'POST':
        fecha = request.POST.get('fecha') or None
        dias_semana = request.POST.getlist('dias_semana')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        tipo_bloque = request.POST.get('tipo_bloque') or 'disponible'
        is_active = request.POST.get('is_active') == 'on'
        bloquear_todo_dia = request.POST.get('bloquear_todo_dia') == 'on'

        if tipo_bloque == 'bloqueado' and bloquear_todo_dia:
            hora_inicio = '00:00'
            hora_fin = '23:59'

        try:
            if dias_semana:
                AgendaHorarioService.create_agenda_horarios_por_dias(
                    dias_semana,
                    hora_inicio,
                    hora_fin,
                    tipo_bloque=tipo_bloque,
                    is_active=is_active
                )
            else:
                AgendaHorarioService.create_agenda_horario(
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    tipo_bloque=tipo_bloque,
                    is_active=is_active
                )
        except ValueError as exc:
            messages.error(request, str(exc))
            return render(
                request,
                'agenda_horarios/agenda_horarios_crear.html',
                {'dias_semana_choices': dias_semana_choices, 'tipos_bloque_choices': tipos_bloque_choices}
            )

        return redirect('agenda_horarios_lista')

    return render(
        request,
        'agenda_horarios/agenda_horarios_crear.html',
        {'dias_semana_choices': dias_semana_choices, 'tipos_bloque_choices': tipos_bloque_choices}
    )

def agenda_horario_editar(request, agenda_horario_id):
    agenda_horario = AgendaHorarioService.get_agenda_horario_by_id(agenda_horario_id)
    dias_semana_choices = AgendaHorarioService.get_dias_semana_choices()
    tipos_bloque_choices = AgendaHorarioService.get_tipos_bloque_choices()

    if not agenda_horario:
        messages.error(request, 'El horario no existe.')
        return redirect('agenda_horarios_lista')

    if request.method == 'POST':
        fecha = request.POST.get('fecha') or None
        dia_semana = request.POST.get('dia_semana') or None
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        tipo_bloque = request.POST.get('tipo_bloque') or 'disponible'
        is_active = request.POST.get('is_active') == 'on'
        bloquear_todo_dia = request.POST.get('bloquear_todo_dia') == 'on'

        if tipo_bloque == 'bloqueado' and bloquear_todo_dia:
            hora_inicio = '00:00'
            hora_fin = '23:59'

        if dia_semana:
            fecha = None

        try:
            AgendaHorarioService.update_agenda_horario(
                agenda_horario_id,
                fecha=fecha,
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                tipo_bloque=tipo_bloque,
                is_active=is_active,
            )
        except ValueError as exc:
            messages.error(request, str(exc))
            return render(
                request,
                'agenda_horarios/agenda_horarios_editar.html',
                {
                    'agenda_horario': agenda_horario,
                    'dias_semana_choices': dias_semana_choices,
                    'tipos_bloque_choices': tipos_bloque_choices,
                    'bloqueo_todo_dia': _es_bloqueo_todo_dia(agenda_horario),
                }
            )

        return redirect('agenda_horarios_lista')

    return render(
        request,
        'agenda_horarios/agenda_horarios_editar.html',
        {
            'agenda_horario': agenda_horario,
            'dias_semana_choices': dias_semana_choices,
            'tipos_bloque_choices': tipos_bloque_choices,
            'bloqueo_todo_dia': _es_bloqueo_todo_dia(agenda_horario),
        }
    )

def agenda_horario_eliminar(request, agenda_horario_id):
    agenda_horario = AgendaHorarioService.get_agenda_horario_by_id(agenda_horario_id)

    if not agenda_horario:
        messages.error(request, 'El horario no existe.')
        return redirect('agenda_horarios_lista')

    if request.method == 'POST':
        try:
            AgendaHorarioService.delete_agenda_horario(agenda_horario_id)
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect('agenda_horarios_lista')

        return redirect('agenda_horarios_lista')

    return render(request, 'agenda_horarios/agenda_horarios_eliminar.html', {'agenda_horario': agenda_horario})
