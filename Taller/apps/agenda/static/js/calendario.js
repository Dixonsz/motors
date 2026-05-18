import {
  byId,
  clearSelect,
  getSelectedInts,
  hideError,
  populateSelect,
  resetMultiSelect,
  setText,
  setValue,
  showError,
  showToast,
  toggleClass,
} from "./calendario/dom.js";
import { fetchFormData, fetchVehicles, postCita } from "./calendario/api.js";
import { buildBusinessHours, isDateTimeBlocked } from "./calendario/horario.js";
import { createCalendar } from "./calendario/calendar.js";

const IDS = {
  calendar: "calendar",
  calendarWrapper: "calendar-wrapper",
  drawer: "drawer-cita",
  drawerLabel: "drawer-fecha-label",
  fecha: "nc-fecha",
  hora: "nc-hora",
  cliente: "nc-cliente",
  vehiculo: "nc-vehiculo",
  estado: "nc-estado",
  servicios: "nc-servicios",
  usuario: "nc-usuario",
  anotaciones: "nc-anotaciones",
  error: "nc-error",
  btnGuardar: "btn-guardar",
  modal: "modal-detalle",
  modalOverlay: "overlay-detalle",
  modalTitle: "modal-title",
  modalEstado: "modal-estado",
  modalCliente: "modal-cliente",
  modalVehiculo: "modal-vehiculo",
  modalLink: "modal-link",
};

const COLORS_BADGE = {
  Pendiente: { bg: "#fff7ed", color: "#c2410c" },
  Confirmada: { bg: "#eff6ff", color: "#1d4ed8" },
  Cancelada: { bg: "#fef2f2", color: "#dc2626" },
  Completada: { bg: "#f0fdf4", color: "#15803d" },
};

const DEFAULT_BADGE = { bg: "#f3f4f6", color: "#374151" };
const CALENDAR_RESIZE_MS = 360;

const config = globalThis.__CALENDARIO_CONFIG__ || {};
const state = { calendar: null };

function getPlaceholder(key, fallback) {
  return config.placeholders?.[key] || fallback;
}

async function loadFormData() {
  try {
    const data = await fetchFormData(config.urlFormData);
    populateSelect(IDS.cliente, data.clientes, {
      labelKey: "nombre",
      placeholder: getPlaceholder("cliente", "Sin cliente"),
    });
    populateSelect(IDS.estado, data.estados, { labelKey: "nombre" });
    populateSelect(IDS.servicios, data.servicios, { labelKey: "nombre" });
    populateSelect(IDS.usuario, data.usuarios, { labelKey: "nombre" });
  } catch (error) {
    console.error("Error cargando datos del formulario.", error);
  }
}

async function loadVehicles(clienteId) {
  clearSelect(IDS.vehiculo, getPlaceholder("vehiculo", "Sin vehiculo"));
  if (!clienteId) return;

  try {
    const vehiculos = await fetchVehicles(config.urlVehiculosBase, clienteId);
    populateSelect(IDS.vehiculo, vehiculos, { labelKey: "placa" });
  } catch (error) {
    console.error("Error cargando vehiculos.", error);
  }
}

function resetDrawerForm() {
  setValue(IDS.anotaciones, "");
  setValue(IDS.cliente, "");
  clearSelect(IDS.vehiculo, getPlaceholder("vehiculo", "Sin vehiculo"));
  resetMultiSelect(IDS.servicios);
  hideError(IDS.error);
}

function updateDrawerLabel(fecha, hora) {
  if (!fecha) {
    setText(IDS.drawerLabel, "");
    return;
  }
  const [year, month, day] = fecha.split("-");
  const labelHora = hora ? ` ${hora}` : "";
  setText(IDS.drawerLabel, `— ${day}/${month}/${year}${labelHora}`);
}

function openDrawer(fecha, hora) {
  if (!fecha || !hora) return;

  const bloqueo = isDateTimeBlocked({
    calendar: state.calendar,
    horarioLaboral: config.horarioLaboral,
    fecha,
    hora,
  });
  if (bloqueo.bloqueado) {
    showToast(`Horario no disponible: ${bloqueo.motivo}`);
    return;
  }

  setValue(IDS.fecha, fecha);
  setValue(IDS.hora, hora);
  resetDrawerForm();
  updateDrawerLabel(fecha, hora);

  toggleClass(IDS.drawer, "open", true);
  toggleClass(IDS.calendarWrapper, "encogido", true);
  setTimeout(() => state.calendar?.updateSize(), CALENDAR_RESIZE_MS);
}

function closeDrawer() {
  toggleClass(IDS.drawer, "open", false);
  toggleClass(IDS.calendarWrapper, "encogido", false);
  setTimeout(() => state.calendar?.updateSize(), CALENDAR_RESIZE_MS);
}

function buildPayload() {
  return {
    fecha: byId(IDS.fecha).value,
    hora_inicio: byId(IDS.hora).value,
    estado_id: Number.parseInt(byId(IDS.estado).value, 10),
    usuario_id: Number.parseInt(byId(IDS.usuario).value, 10),
    cliente_id: toOptionalInt(byId(IDS.cliente).value),
    vehiculo_id: toOptionalInt(byId(IDS.vehiculo).value),
    anotaciones: byId(IDS.anotaciones).value,
    servicios_id: getSelectedInts(IDS.servicios),
  };
}

function toOptionalInt(value) {
  const parsed = Number.parseInt(value, 10);
  return Number.isNaN(parsed) ? null : parsed;
}

function validateRequired(payload) {
  if (!payload.fecha || !payload.hora_inicio) {
    return "La fecha y la hora son obligatorias.";
  }
  if (!payload.estado_id) {
    return "Debe seleccionar un estado.";
  }
  if (!payload.usuario_id) {
    return "Debe asignar un usuario.";
  }
  return null;
}

async function handleSave() {
  hideError(IDS.error);
  const payload = buildPayload();
  const errorMsg = validateRequired(payload);
  if (errorMsg) {
    showError(IDS.error, errorMsg);
    return;
  }

  const bloqueo = isDateTimeBlocked({
    calendar: state.calendar,
    horarioLaboral: config.horarioLaboral,
    fecha: payload.fecha,
    hora: payload.hora_inicio,
  });
  if (bloqueo.bloqueado) {
    showError(IDS.error, `Horario no disponible: ${bloqueo.motivo}`);
    return;
  }

  const btn = byId(IDS.btnGuardar);
  btn.disabled = true;
  btn.textContent = "Guardando...";

  try {
    const result = await postCita({
      url: config.urlCrear,
      payload,
      csrfToken: config.csrfToken,
    });

    if (result.ok) {
      closeDrawer();
      state.calendar?.refetchEvents();
    } else {
      showError(IDS.error, result.data?.error || "Error al guardar la cita.");
    }
  } catch (error) {
    showError(IDS.error, "Error de red. Intente de nuevo.");
    console.error(error);
  } finally {
    btn.disabled = false;
    btn.textContent = "Guardar cita";
  }
}

function openModal(event) {
  const props = event.extendedProps || {};
  const estado = props.estado;
  const colores = COLORS_BADGE[estado] || DEFAULT_BADGE;
  const baseUrl = config.urlCitaEditarBase || "/agenda/citas/editar/";

  setText(IDS.modalTitle, event.title);
  setText(IDS.modalCliente, props.cliente || "Sin cliente");
  setText(IDS.modalVehiculo, props.vehiculo || "Sin vehiculo");

  const badgeEl = byId(IDS.modalEstado);
  badgeEl.textContent = estado;
  badgeEl.style.background = colores.bg;
  badgeEl.style.color = colores.color;

  byId(IDS.modalLink).href = `${baseUrl}${event.id}/`;
  toggleClass(IDS.modal, "active", true);
  toggleClass(IDS.modalOverlay, "active", true);
}

function closeModal() {
  toggleClass(IDS.modal, "active", false);
  toggleClass(IDS.modalOverlay, "active", false);
}

function handleEventClick(event) {
  if (event.extendedProps?.bloqueo) {
    showToast(`${event.title}`);
    return;
  }
  openModal(event);
}

function initCalendar() {
  const businessHours = buildBusinessHours(config.horarioLaboral);
  state.calendar = createCalendar({
    element: byId(IDS.calendar),
    eventosUrl: config.urlEventos,
    businessHours,
    slotMinTime: businessHours?.startTime,
    slotMaxTime: businessHours?.endTime,
    onDateSelected: ({ fecha, hora }) => openDrawer(fecha, hora),
    onEventClick: handleEventClick,
  });
  state.calendar.render();
}

function bindUi() {
  byId(IDS.btnGuardar).addEventListener("click", handleSave);
  byId(IDS.cliente).addEventListener("change", (event) => {
    loadVehicles(event.target.value);
  });

  document.querySelectorAll("[data-action='close-drawer']").forEach((btn) => {
    btn.addEventListener("click", closeDrawer);
  });
  document.querySelectorAll("[data-action='close-modal']").forEach((btn) => {
    btn.addEventListener("click", closeModal);
  });
}

function init() {
  loadFormData();
  initCalendar();
  bindUi();
}

document.addEventListener("DOMContentLoaded", init);