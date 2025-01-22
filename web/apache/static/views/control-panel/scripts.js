// URL base de la API
const apiUrl = "/api/peliculas"; // Ajustar según la URL de tu API

// Función para insertar una película
// Función para insertar una película
function insertMovie(event) {
  event.preventDefault(); // Evitar que el formulario recargue la página

  // Obtener los valores del formulario
  const nombre = document.getElementById("titulo").value;
  const sinopsis = document.getElementById("sinopsis").value;
  const categoria = document.getElementById("genero").value;
  const portada = document.getElementById("portada").files[0]; // Obtener el archivo de la portada

  // Crear un FormData para enviar los datos incluyendo el archivo
  const formData = new FormData();
  formData.append("nombre", nombre); // Nombre de la película
  formData.append("sinopsis", sinopsis); // Sinopsis de la película
  formData.append("categoria", categoria); // Categoría de la película
  formData.append("fichero", portada); // Archivo de la portada

  // Enviar el archivo a la ruta /api/upload para guardarlo
  fetch("/api/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.status === "OK") {
        alert("Película guardada con éxito");
        cerrarFormulario();
        agregarFila(nombre, categoria, sinopsis, URL.createObjectURL(portada)); // Mostrar la película en la tabla
      } else {
        alert("Hubo un error al guardar la película");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Se ha producido un error al subir la portada");
    });
}

// Función para agregar una fila a la tabla
function agregarFila(nombre, categoria, sinopsis, portadaURL) {
  const tableBody = document.getElementById("movie-list");

  // Crear una nueva fila en la tabla
  const row = document.createElement("tr");

  // Crear las celdas para el nombre, categoría, sinopsis, portada
  const tdNombre = document.createElement("td");
  tdNombre.textContent = nombre;
  const tdCategoria = document.createElement("td");
  tdCategoria.textContent = categoria;
  const tdSinopsis = document.createElement("td");
  tdSinopsis.textContent = sinopsis;
  const tdPortada = document.createElement("td");
  const img = document.createElement("img");
  img.src = portadaURL; // Usar la URL de la imagen subida
  img.alt = "Portada";
  img.width = 100; // Puedes ajustar el tamaño de la imagen si lo deseas
  tdPortada.appendChild(img);

  // Agregar las celdas a la fila
  row.appendChild(tdNombre);
  row.appendChild(tdCategoria);
  row.appendChild(tdSinopsis);
  row.appendChild(tdPortada);

  // Agregar la fila a la tabla
  tableBody.appendChild(row);
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
