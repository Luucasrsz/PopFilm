function insertMovie() {
  const nombre = document.getElementById("titulo").value;
  const sinopsis = document.getElementById("sinopsis").value;
  const categoria = document.getElementById("genero").value;
  const anio = document.getElementById("anio").value;

  // Preparar los datos a enviar
  const datos = JSON.stringify({
    nombre: nombre,
    sinopsis: sinopsis,
    categoria: categoria,
    anio: anio,
  });

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: datos,
  };

  fetch("/api/peliculas", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status === "OK") {
        alert("Película guardada con éxito");
        cerrarFormulario();
        agregarFila(nombre, categoria, anio);
      } else {
        alert("La película no se ha guardado");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Se ha producido un error");
    });
}

// Agregar fila a la tabla dinámicamente
function agregarFila(nombre, categoria, anio) {
  const tableBody = document.getElementById("movie-list");
  const newRow = `
      <tr>
        <td>${nombre}</td>
        <td>${categoria}</td>
        <td>${anio}</td>
        <td>
          <button class="icon-button" onclick="abrirFormulario()">
            <span class="icon">✏️</span>
          </button>
          <button class="icon-button" onclick="deleteMovie(this)">
            <span class="icon">🗑️</span>
          </button>
        </td>
      </tr>
    `;

  tableBody.insertAdjacentHTML("beforeend", newRow);
}

// Eliminar fila de la tabla
function deleteMovie(button) {
  const row = button.closest("tr");
  row.remove();
}

// Abrir el formulario modal
function abrirFormulario() {
  document.getElementById("modal-form").style.display = "flex";
}

// Cerrar el formulario modal
function cerrarFormulario() {
  document.getElementById("modal-form").style.display = "none";
}
