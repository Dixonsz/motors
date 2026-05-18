function toggleCampos() {
  const tipo = document.getElementById("tipo").value;
  const camposHorario = document.getElementById("campos-horario");
  const camposLaboral = document.getElementById("campos-laboral");
  const campoFechaFin = document.getElementById("campo-fecha-fin");
  const campoFechaInicio = document.getElementById("campo-fecha-inicio");
  const campoCapacidad = document.getElementById("campo-capacidad");
  const campoRecurrencia = document.getElementById("campo-recurrencia");
  const recurrencia = document.getElementById("recurrencia");
  const fechaInicio = document.getElementById("fecha_inicio");

  const esFranja = tipo === "franja";
  const esLaboral = tipo === "laboral";
  const esDiaCompleto = tipo === "dia_completo";

  camposHorario.style.display = esFranja || esLaboral ? "block" : "none";
  camposLaboral.style.display = esLaboral ? "block" : "none";
  campoCapacidad.style.display = esFranja ? "block" : "none";
  campoFechaFin.style.display = esDiaCompleto ? "block" : "none";
  campoFechaInicio.style.display = esLaboral ? "none" : "block";
  campoRecurrencia.style.display = esLaboral ? "none" : "block";

  fechaInicio.required = !esLaboral;
  if (esLaboral) {
    fechaInicio.value = "";
  }

  if (esLaboral) {
    recurrencia.value = "diaria";
  }
}

document.addEventListener("DOMContentLoaded", toggleCampos);
