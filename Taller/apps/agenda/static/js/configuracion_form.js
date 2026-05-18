const IDS = {
  tipo: "tipo",
  camposHorario: "campos-horario",
  camposLaboral: "campos-laboral",
  campoFechaFin: "campo-fecha-fin",
  campoFechaInicio: "campo-fecha-inicio",
  campoCapacidad: "campo-capacidad",
  campoRecurrencia: "campo-recurrencia",
  recurrencia: "recurrencia",
  fechaInicio: "fecha_inicio",
};

function byId(id) {
  return document.getElementById(id);
}

function setDisplay(id, visible) {
  const el = byId(id);
  if (el) el.style.display = visible ? "block" : "none";
}

function setRequired(id, required) {
  const el = byId(id);
  if (el) el.required = required;
}

function setValue(id, value) {
  const el = byId(id);
  if (el) el.value = value;
}

function getState() {
  const tipo = byId(IDS.tipo)?.value || "";
  return {
    tipo,
    esFranja: tipo === "franja",
    esLaboral: tipo === "laboral",
    esDiaCompleto: tipo === "dia_completo",
  };
}

function applyVisibility(state) {
  setDisplay(IDS.camposHorario, state.esFranja || state.esLaboral);
  setDisplay(IDS.camposLaboral, state.esLaboral);
  setDisplay(IDS.campoCapacidad, state.esFranja);
  setDisplay(IDS.campoFechaFin, state.esDiaCompleto);
  setDisplay(IDS.campoFechaInicio, !state.esLaboral);
  setDisplay(IDS.campoRecurrencia, !state.esLaboral);
}

function applyDefaults(state) {
  setRequired(IDS.fechaInicio, !state.esLaboral);
  if (state.esLaboral) {
    setValue(IDS.fechaInicio, "");
    setValue(IDS.recurrencia, "diaria");
  }
}

function toggleCampos() {
  const state = getState();
  applyVisibility(state);
  applyDefaults(state);
}

function init() {
  const tipo = byId(IDS.tipo);
  if (tipo) tipo.addEventListener("change", toggleCampos);
  toggleCampos();
}

document.addEventListener("DOMContentLoaded", init);
