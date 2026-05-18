async function fetchJson(url, options) {
  const res = await fetch(url, options);
  const data = await res.json();
  return { res, data };
}

export async function fetchFormData(url) {
  const { res, data } = await fetchJson(url);
  if (!res.ok) throw new Error("form-data");
  return data;
}

export async function fetchVehicles(urlBase, clienteId) {
  const { res, data } = await fetchJson(`${urlBase}${clienteId}/`);
  if (!res.ok) throw new Error("vehiculos");
  return data.vehiculos || [];
}

export async function postCita({ url, payload, csrfToken }) {
  const { res, data } = await fetchJson(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(payload),
  });

  return { ok: res.ok, data };
}
