function toggleCampos() {
  const tipo = document.getElementById("tipo").value;
  const franja = document.getElementById("campos-franja");
  franja.style.display = tipo === "franja" ? "block" : "none";
}

document.addEventListener("DOMContentLoaded", toggleCampos);
