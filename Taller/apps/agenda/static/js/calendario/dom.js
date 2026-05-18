const TOAST_ID = "fc-toast";
const TOAST_DURATION_MS = 3000;
const TOAST_STYLES = [
  "position:fixed",
  "bottom:2rem",
  "left:50%",
  "transform:translateX(-50%)",
  "background:#1f2937",
  "color:#fff",
  "padding:.75rem 1.5rem",
  "border-radius:.5rem",
  "font-size:.9rem",
  "z-index:9999",
  "box-shadow:0 4px 12px rgba(0,0,0,.3)",
  "transition:opacity .3s",
].join(";");

export function byId(id) {
  return document.getElementById(id);
}

export function setText(id, text) {
  const el = byId(id);
  if (el) el.textContent = text;
}

export function setValue(id, value) {
  const el = byId(id);
  if (el) el.value = value;
}

export function setHtml(id, html) {
  const el = byId(id);
  if (el) el.innerHTML = html;
}

export function toggleClass(id, className, enabled) {
  const el = byId(id);
  if (el) el.classList.toggle(className, enabled);
}

export function clearSelect(id, placeholder) {
  const sel = byId(id);
  if (!sel) return;
  sel.innerHTML = "";
  if (placeholder !== null && placeholder !== undefined) {
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = placeholder;
    sel.appendChild(opt);
  }
}

export function populateSelect(id, items, options) {
  const sel = byId(id);
  if (!sel) return;
  clearSelect(id, options?.placeholder ?? null);
  items.forEach((item) => {
    const opt = document.createElement("option");
    opt.value = item[options?.valueKey ?? "id"];
    opt.textContent = item[options.labelKey];
    sel.appendChild(opt);
  });
}

export function resetMultiSelect(id) {
  const sel = byId(id);
  if (!sel) return;
  Array.from(sel.options).forEach((opt) => {
    opt.selected = false;
  });
}

export function getSelectedInts(id) {
  const sel = byId(id);
  if (!sel) return [];
  return Array.from(sel.selectedOptions).map((opt) => Number.parseInt(opt.value, 10));
}

export function showError(id, message) {
  const el = byId(id);
  if (!el) return;
  el.textContent = message;
  el.classList.add("visible");
}

export function hideError(id) {
  const el = byId(id);
  if (el) el.classList.remove("visible");
}

export function showToast(message) {
  let toast = byId(TOAST_ID);
  if (!toast) {
    toast = document.createElement("div");
    toast.id = TOAST_ID;
    toast.style.cssText = TOAST_STYLES;
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.style.opacity = "1";
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.style.opacity = "0";
  }, TOAST_DURATION_MS);
}
