from django.http import JsonResponse
from django.shortcuts import render
from ...models.cita import Cita

def citas_calendario(request):
    citas = Cita.objects.select_related('cliente', 'vehiculo', 'estado').all()

    colores = {
        'Pendiente': '#FFC300',  # Amarillo
        'Confirmada': '#33C1FF',  # Azul
        'Cancelada': '#FF5733',   # Rojo
        'Completada': '#28A745',  # Verde
    }
    eventos = []
    for cita in citas:
        eventos.append({
            'id': cita.id,
            'title': f"{cita.cliente.nombre if cita.cliente else cita.vehiculo.placa} - {cita.estado.nombre}",
            'start': f"{cita.fecha}T{cita.hora_inicio}",
            'color': colores.get(cita.estado.nombre.lower(), '#6b7280'),  # Gris por defecto
            "extendedProps": {
                "estado": cita.estado.nombre, 
                "vehiculo": cita.vehiculo.placa if cita.vehiculo else "Sin vehículo",
                "cliente": cita.cliente.nombre if cita.cliente else "Sin cliente",
            }
        })
    
    return JsonResponse(eventos, safe=False)

def calendario_view(request):
    return render(request, 'citas/calendario/citas_calendario.html')