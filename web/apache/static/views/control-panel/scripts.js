// URL base de la API
const apiUrl = "/api/peliculas"; // Ajustar según la URL de tu API

// Función para insertar una película
function insertMovie(event) {
  event.preventDefault(); // Evitar que el formulario recargue la página

  // Obtener los valores del formulario
  const nombre = document.getElementById("titulo").value;
  const sinopsis = document.getElementById("sinopsis").value;
  const categoria = document.getElementById("genero").value;
  const portada = document.getElementById("portada").files[0]; // Obtenemos el archivo de la portada

  // Crear un FormData para enviar los datos incluyendo el archivo
  const formData = new FormData();
  formData.append("nombre", nombre);
  formData.append("sinopsis", sinopsis);
  formData.append("categoria", categoria);
  formData.append("portada", portada);

  // Configurar la solicitud para enviar los datos
  const requestOptions = {
    method: "POST",
    body: formData,
  };

  // Enviar los datos al servidor
  fetch(apiUrl, requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status === "OK") {
        alert("Película guardada con éxito");
        cerrarFormulario();
        agregarFila(nombre, categoria, sinopsis, URL.createObjectURL(portada)); // Mostrar la película en la tabla
      } else {
        alert("La película no se ha guardado");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Se ha producido un error");
    });
}

// Función para agregar una fila a la tabla
function agregarFila(nombre, categoria, sinopsis, portadaUrl) {
  const movieList = document.getElementById("movie-list");
  const row = document.createElement("tr");

  row.innerHTML = `
    <td>${nombre}</td>
    <td>${categoria}</td>
    <td>${sinopsis}</td>
    <td><img src="${portadaUrl}" alt="Portada" width="50" /></td>
    <td>
      <button onclick="deleteMovie(this)">Eliminar</button>
    </td>
  `;

  movieList.appendChild(row);
}

// Función para eliminar una película de la tabla
function deleteMovie(button) {
  const row = button.closest("tr"); // Encuentra la fila más cercana al botón
  const movieId = row.dataset.id; // Asumir que cada fila tiene un 'data-id' con el ID de la película

  // Eliminar película desde la API
  fetch(`/api/peliculas/${movieId}`, { method: "DELETE" })
    .then((response) => response.json())
    .then((result) => {
      if (result.status === "OK") {
        row.remove(); // Eliminar la fila de la tabla
      } else {
        alert("La película no se ha eliminado");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Se ha producido un error al eliminar la película");
    });
}

// Función para abrir el formulario modal
function abrirFormulario() {
  document.getElementById("modal-form").style.display = "flex";
}

// Función para cerrar el formulario modal
function cerrarFormulario() {
  document.getElementById("modal-form").style.display = "none";
}
