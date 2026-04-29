

const COLORES_BADGE = {
  Pendiente: { bg: "#fff7ed", color: "#c2410c" },
  Confirmada: { bg: "#eff6ff", color: "#1d4ed8" },
  Cancelada: { bg: "#fef2f2", color: "#dc2626" },
  Completada: { bg: "#f0fdf4", color: "#15803d" },
};

let calendarInstance = null;

async function cargarFormData() {
  try {
    const res = await fetch(URL_FORM_DATA);
    const data = await res.json();

    poblarSelect("nc-cliente", data.clientes, "nombre", "Sin cliente");
    poblarSelect("nc-estado", data.estados, "nombre", null);
    poblarSelect("nc-servicios", data.servicios, "nombre", null, true);
    poblarSelect("nc-usuario", data.usuarios, "nombre", null);

    document
      .getElementById("nc-cliente")
      .addEventListener("change", cargarVehiculos);
  } catch {
    console.error("Error cargando datos del formulario.");
  }
}

function poblarSelect(
  id,
  items,
  labelKey,
  opcionVacia = null,
  multiple = false,
) {
  const sel = document.getElementById(id);
  sel.innerHTML = "";
  if (opcionVacia !== null) {
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = opcionVacia;
    sel.appendChild(opt);
  }
  items.forEach((item) => {
    const opt = document.createElement("option");
    opt.value = item.id;
    opt.textContent = item[labelKey];
    sel.appendChild(opt);
  });
}

async function cargarVehiculos() {
  const clienteId = document.getElementById("nc-cliente").value;
  const sel = document.getElementById("nc-vehiculo");
  sel.innerHTML = '<option value="">Sin vehículo</option>';

  if (!clienteId) return;

  try {
    const res = await fetch(`${URL_VEHICULOS}${clienteId}/`);
    const data = await res.json();
    data.vehiculos.forEach((v) => {
      const opt = document.createElement("option");
      opt.value = v.id;
      opt.textContent = v.placa;
      sel.appendChild(opt);
    });
  } catch {
    console.error("Error cargando vehículos.");
  }
}

function abrirDrawer(fecha = "", hora = "") {
  document.getElementById("nc-fecha").value = fecha;
  document.getElementById("nc-hora").value = hora;
  document.getElementById("nc-anotaciones").value = "";
  document.getElementById("nc-cliente").value = "";
  document.getElementById("nc-vehiculo").innerHTML =
    '<option value="">Sin vehículo</option>';
  Array.from(document.getElementById("nc-servicios").options).forEach(
    (o) => (o.selected = false),
  );
  ocultarError();

  if (fecha) {
    const [y, m, d] = fecha.split("-");
    document.getElementById("drawer-fecha-label").textContent =
      `— ${d}/${m}/${y}${hora ? " " + hora : ""}`;
  } else {
    document.getElementById("drawer-fecha-label").textContent = "";
  }

  document.getElementById("drawer-cita").classList.add("open");
  document.getElementById("calendar-wrapper").classList.add("encogido");
  setTimeout(() => calendarInstance?.updateSize(), 360);
}

function cerrarDrawer() {
  document.getElementById("drawer-cita").classList.remove("open");
  document.getElementById("calendar-wrapper").classList.remove("encogido");
  setTimeout(() => calendarInstance?.updateSize(), 360);
}

async function guardarCita() {
  ocultarError();

  const fecha = document.getElementById("nc-fecha").value;
  const hora = document.getElementById("nc-hora").value;
  const estadoId = document.getElementById("nc-estado").value;
  const usuarioId = document.getElementById("nc-usuario").value;

  if (!fecha || !hora) {
    mostrarError("La fecha y la hora son obligatorias.");
    return;
  }
  if (!estadoId) {
    mostrarError("Debe seleccionar un estado.");
    return;
  }
  if (!usuarioId) {
    mostrarError("Debe asignar un usuario.");
    return;
  }

  const serviciosId = Array.from(
    document.getElementById("nc-servicios").selectedOptions,
  ).map((o) => parseInt(o.value));

  const payload = {
    fecha,
    hora_inicio: hora,
    estado_id: parseInt(estadoId),
    usuario_id: parseInt(usuarioId),
    cliente_id: parseInt(document.getElementById("nc-cliente").value) || null,
    vehiculo_id: parseInt(document.getElementById("nc-vehiculo").value) || null,
    anotaciones: document.getElementById("nc-anotaciones").value,
    servicios_id: serviciosId,
  };

  const btn = document.getElementById("btn-guardar");
  btn.disabled = true;
  btn.textContent = "Guardando...";

  try {
    const res = await fetch(URL_CREAR, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": CSRF_TOKEN,
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!res.ok) {
      mostrarError(data.error || "Error al guardar la cita.");
    } else {
      cerrarDrawer();
      calendarInstance.refetchEvents();
    }
  } catch {
    mostrarError("Error de red. Intente de nuevo.");
  } finally {
    btn.disabled = false;
    btn.textContent = "Guardar cita";
  }
}

function mostrarError(msg) {
  const el = document.getElementById("nc-error");
  el.textContent = msg;
  el.classList.add("visible");
}

function ocultarError() {
  document.getElementById("nc-error").classList.remove("visible");
}

function abrirModalDetalle(event) {
  const props = event.extendedProps;
  const estado = props.estado;
  const colores = COLORES_BADGE[estado] || { bg: "#f3f4f6", color: "#374151" };

  document.getElementById("modal-title").textContent = event.title;
  document.getElementById("modal-cliente").textContent =
    props.cliente || "Sin cliente";
  document.getElementById("modal-vehiculo").textContent =
    props.vehiculo || "Sin vehículo";
  document.getElementById("modal-link").href = `/citas/${event.id}/`;

  const badgeEl = document.getElementById("modal-estado");
  badgeEl.textContent = estado;
  badgeEl.style.background = colores.bg;
  badgeEl.style.color = colores.color;

  document.getElementById("modal-detalle").classList.add("active");
  document.getElementById("overlay-detalle").classList.add("active");
}

function cerrarModalDetalle() {
  document.getElementById("modal-detalle").classList.remove("active");
  document.getElementById("overlay-detalle").classList.remove("active");
}

document.addEventListener("DOMContentLoaded", function () {
  cargarFormData();

  calendarInstance = new FullCalendar.Calendar(
    document.getElementById("calendar"),
    {
      initialView: "timeGridWeek",
      locale: "es",
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay",
      },
      selectable: true,
      selectMirror: true,
      height: "auto",

      dateClick: function (info) {
        const fecha = info.dateStr.slice(0, 10);
        const hora = info.dateStr.length > 10 ? info.dateStr.slice(11, 16) : "";
        abrirDrawer(fecha, hora);
      },

      select: function (info) {
        const fecha = info.startStr.slice(0, 10);
        const hora =
          info.startStr.length > 10 ? info.startStr.slice(11, 16) : "";
        abrirDrawer(fecha, hora);
      },

      events: URL_EVENTOS,

      eventClick: function (info) {
        abrirModalDetalle(info.event);
      },
    },
  );

  calendarInstance.render();
});
