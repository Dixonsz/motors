function extractFechaHora(dateStr) {
  const fecha = dateStr.slice(0, 10);
  const hora = dateStr.length > 10 ? dateStr.slice(11, 16) : "";
  return { fecha, hora };
}

export function createCalendar({
  element,
  eventosUrl,
  businessHours,
  slotMinTime,
  slotMaxTime,
  onDateSelected,
  onEventClick,
}) {
  const calendarOptions = {
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
    events: eventosUrl,
    dateClick: (info) => onDateSelected(extractFechaHora(info.dateStr)),
    select: (info) => onDateSelected(extractFechaHora(info.startStr)),
    eventClick: (info) => onEventClick(info.event),
  };

  // Solo agregar si están definidos
  if (businessHours) calendarOptions.businessHours = businessHours;
  if (slotMinTime) calendarOptions.slotMinTime = slotMinTime;
  if (slotMaxTime) calendarOptions.slotMaxTime = slotMaxTime;

  return new FullCalendar.Calendar(element, calendarOptions);
}

