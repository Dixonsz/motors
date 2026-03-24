from django.shortcuts import render
from django.db.models import Count, Q

from ...models import CategoriaServicio, Servicio


def inicio(request):
    categoria_id = request.GET.get('categoria')

    categorias = CategoriaServicio.objects.filter(is_active=True).annotate(
        servicios_activos_count=Count('servicios', filter=Q(servicios__is_active=True))
    ).order_by('nombre')
    servicios = (
        Servicio.objects.filter(is_active=True, categoria_servicio__is_active=True)
        .select_related('categoria_servicio')
        .order_by('categoria_servicio__nombre', 'nombre')
    )

    categoria_activa = None
    if categoria_id:
        try:
            categoria_id_int = int(categoria_id)
        except (TypeError, ValueError):
            categoria_id_int = None

        if categoria_id_int is not None:
            servicios = servicios.filter(categoria_servicio_id=categoria_id_int)
            categoria_activa = categorias.filter(id=categoria_id_int).first()

    context = {
        'categorias': categorias,
        'servicios': servicios,
        'total_servicios': servicios.count(),
        'categoria_activa': categoria_activa,
        'categoria_id_activa': str(categoria_id) if categoria_id else '',
    }
    return render(request, 'inicio/index.html', context)