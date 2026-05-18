function toJsDay(pyDay) {
  return (pyDay + 1) % 7;
}

function toPyDay(jsDay) {
  return (jsDay + 6) % 7;
}

export function buildBusinessHours(horarioLaboral) {
  if (!horarioLaboral) return null;
  const diasLaborales = horarioLaboral.dias_laborales || [];
  if (!diasLaborales.length) return null;

  return {
    daysOfWeek: diasLaborales.map(toJsDay),
    startTime: horarioLaboral.hora_inicio || "00:00",
    endTime: horarioLaboral.hora_fin || "24:00",
  };
}

function checkHorarioLaboral({ horarioLaboral, fecha, hora }) {
  if (!horarioLaboral) return null;

  const dias = horarioLaboral.dias_laborales || [];
  const diaJs = new Date(`${fecha}T00:00:00`).getDay();
  const diaPy = toPyDay(diaJs);

  if (dias.length && !dias.includes(diaPy)) {
    return { bloqueado: true, motivo: "Fuera de horario laboral" };
  }

  if (horarioLaboral.hora_inicio && horarioLaboral.hora_fin) {
    if (hora < horarioLaboral.hora_inicio || hora >= horarioLaboral.hora_fin) {
      return { bloqueado: true, motivo: "Fuera de horario laboral" };
    }
  }

  return null;
}

function getBlocks(calendar) {
  if (!calendar) return [];
  return calendar.getEvents().filter((event) => event.extendedProps?.bloqueo === true);
}

function checkFullDayBlock(bloqueo, fecha) {
  const inicioStr = bloqueo.startStr.slice(0, 10);
  const finDate = bloqueo.end ? new Date(bloqueo.end) : new Date(bloqueo.start);
  finDate.setDate(finDate.getDate() - 1);
  const finStr = finDate.toISOString().slice(0, 10);

  if (fecha >= inicioStr && fecha <= finStr) {
    return { bloqueado: true, motivo: bloqueo.title };
  }

  return null;
}

function checkTimeBlock(bloqueo, fecha, hora) {
  const citaStr = `${fecha}T${hora}`;
  const inicioStr = bloqueo.startStr.slice(0, 16);
  const finStr = bloqueo.endStr ? bloqueo.endStr.slice(0, 16) : inicioStr;

  if (citaStr < inicioStr || citaStr >= finStr) return null;

  const capacidad = bloqueo.extendedProps?.capacidad_maxima;
  if (capacidad) return null;

  return { bloqueado: true, motivo: bloqueo.title };
}

export function isDateTimeBlocked({ calendar, horarioLaboral, fecha, hora }) {
  const laboral = checkHorarioLaboral({ horarioLaboral, fecha, hora });
  if (laboral) return laboral;

  for (const bloqueo of getBlocks(calendar)) {
    const esDiaCompleto = bloqueo.extendedProps?.tipo === "dia_completo";
    const resultado = esDiaCompleto
      ? checkFullDayBlock(bloqueo, fecha)
      : checkTimeBlock(bloqueo, fecha, hora);

    if (resultado) return resultado;
  }

  return { bloqueado: false };
}
