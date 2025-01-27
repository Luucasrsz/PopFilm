var myHeaders = new Headers();

// URL base de la API
const apiUrl = "/api/peliculas"; // Ajustar según la URL de tu API

// Función para insertar una película
function insertMovie(event) {
  event.preventDefault(); // Evitar que el formulario recargue la página

  // Obtener los valores del formulario
  const nombre = document.getElementById("titulo").value;
  const sinopsis = document.getElementById("sinopsis").value;
  const categoria = document.getElementById("categoria").value;
  const precio = parseFloat(document.getElementById("precio").value);
  const portada = document.getElementById("portada").files[0]; // Obtener el archivo de la portada

  // FormData para enviar el archivo de la portada
  const formData = new FormData();
  formData.append("nombre", nombre);
  formData.append("sinopsis", sinopsis);
  formData.append("categoria", categoria);
  formData.append("precio", precio);
  formData.append("portada", portada);

  fetch(apiUrl, {
    method: "POST",
    headers: myHeaders,
    body: formData,
  })
    .then((response) => response.json())
    .then((result) => {
      if (result.status === "OK") {
        alert("Película guardada con éxito");
        cerrarFormulario();
        agregarFila(
          nombre,
          categoria,
          sinopsis,
          precio,
          portada.name // Mostrar el nombre del archivo como la portada
        ); // Mostrar la película en la tabla
      } else {
        alert("Hubo un error al guardar la película");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Se ha producido un error al subir la portada");
    });
}

// Función para editar una película
let peliculaId; // Variable global para almacenar el ID de la película

// Función para editar una película
function editarPelicula(id) {
  console.log("EDITAR")
  console.log(id)
  peliculaId = id; // Almacenar el ID al editar la película
  fetch(`/api/pelicula/${id}`, {
    method: 'GET'
  })
    .then(response => response.json())
    .then(pelicula => {
      console.log(pelicula.nombre)
      // Rellenar los campos del formulario con los datos actuales de la película
      document.getElementById("titulo").value = pelicula.nombre;
      document.getElementById("sinopsis").value = pelicula.sinopsis;
      document.getElementById("categoria").value = pelicula.categoria;
      document.getElementById("precio").value = pelicula.precio;

      // Mostrar la portada actual (si existe)
      const portadaImagen = document.getElementById("portada-imagen");
      if (pelicula.portada) {
        portadaImagen.src = pelicula.portada;  // Ruta de la imagen de la portada
        portadaImagen.style.display = 'block';  // Mostrar la imagen
      } else {
        portadaImagen.style.display = 'none';  // Ocultar si no hay portada
      }

      // Cambiar el botón de "Guardar" a "Actualizar"
      document.getElementById("submit-btn").textContent = "Actualizar";

      // Cambiar la función del formulario a guardarCambios
      document.getElementById("movie-form").onsubmit = guardarCambios;

      // Abrir el formulario modal
      abrirFormulario();
    })
    .catch(error => {
      console.error('Error al obtener los detalles de la película:', error);
    });
}

// Función para guardar los cambios de una película
// Función para guardar los cambios de una película
function guardarCambios(event) {
  event.preventDefault(); // Evitar que se recargue la página

  const nombre = document.getElementById("titulo").value;
  const sinopsis = document.getElementById("sinopsis").value;
  const categoria = document.getElementById("categoria").value;
  const precio = parseFloat(document.getElementById("precio").value);
  const portada = document.getElementById("portada").files[0];  // Obtener el archivo de la portada

  const formData = new FormData();
  formData.append("id", peliculaId);  // ID de la película que se está editando
  formData.append("nombre", nombre);
  formData.append("sinopsis", sinopsis);
  formData.append("categoria", categoria);
  formData.append("precio", precio);
  
  // Si se selecciona una nueva portada, se agrega
  if (portada) {
    formData.append("portada", portada);
  }

  // Enviar los datos al servidor
  fetch(`/api/peliculas`, {
    method: 'PUT',
    body: formData
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      return response.json();
    })
    .then(result => {
      console.log(result);
      if (result.status === "OK") {
        alert("Película actualizada con éxito");
        cerrarFormulario();
        cargarPeliculas(); // Recargar las películas para ver los cambios
      } else {
        alert(`Hubo un error al actualizar la película: ${result.message || "Error desconocido"}`);
      }
    })
    .catch(error => {
      console.error('Error al actualizar la película:', error);
      alert(`Se ha producido un error: ${error.message || "Error desconocido"}`);
    });
}




// Función para agregar una fila a la tabla de películas
function agregarFila(nombre, categoria, sinopsis, precio, portada, id) {
  const tableBody = document.getElementById("movie-list");

  // Crear una nueva fila en la tabla
  const row = document.createElement("tr");

  // Crear las celdas para el nombre, categoría, sinopsis
  const tdNombre = document.createElement("td");
  tdNombre.textContent = nombre;
  const tdCategoria = document.createElement("td");
  tdCategoria.textContent = categoria;
  const tdSinopsis = document.createElement("td");
  tdSinopsis.textContent = sinopsis;

  // Crear la celda para el precio
  const tdPrecio = document.createElement("td");
  tdPrecio.textContent = precio;  // Asegúrate de que el precio vaya aquí

  // Crear la celda para la portada
  const tdPortada = document.createElement("td");
  tdPortada.textContent = portada;  // Mostrar el nombre de la portada

  // Crear las celdas para las acciones (editar y eliminar)
  const tdAcciones = document.createElement("td");

  // Botón de editar
  const btnEditar = document.createElement("button");
  btnEditar.textContent = "Editar";
  btnEditar.onclick = function() {
    console.log("ID para editar:", id);  // Verificar si el id se pasa correctamente
    editarPelicula(id);  // Llamar a editarPelicula con el id
  };

  // Botón de eliminar
  const btnEliminar = document.createElement("button");
  btnEliminar.textContent = "Eliminar";
  btnEliminar.addEventListener("click", function() {
    eliminarPelicula(id);
  });

  // Añadir los botones a la celda de acciones
  tdAcciones.appendChild(btnEditar);
  tdAcciones.appendChild(btnEliminar);

  // Agregar las celdas a la fila en el orden correcto
  row.appendChild(tdNombre);     // Título
  row.appendChild(tdCategoria);  // Categoría
  row.appendChild(tdSinopsis);   // Sinopsis
  row.appendChild(tdPrecio);     // Precio
  row.appendChild(tdPortada);    // Portada
  row.appendChild(tdAcciones);   // Acciones

  // Agregar la fila a la tabla
  tableBody.appendChild(row);
}

// Función para cargar todas las películas
function cargarPeliculas() {
  fetch("/api/peliculas")
    .then(response => response.json())
    .then(peliculas => {
      const tableBody = document.getElementById("movie-list");
      tableBody.innerHTML = '';
      peliculas.forEach(pelicula => {
        agregarFila(pelicula.nombre, pelicula.categoria, pelicula.sinopsis, pelicula.precio, pelicula.portada, pelicula.id);
      });
    })
    .catch(error => console.error('Error al cargar las películas:', error));
}

// Función para eliminar una película
function eliminarPelicula(id) {
  console.log("ELIMINAR")
  console.log(id)
  fetch(`/api/peliculas/${id}`, {
    method: 'DELETE'
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === "OK") {
      alert("Película eliminada");
      cargarPeliculas();  // Recargar la lista de películas
    } else {
      alert("Error al eliminar la película");
    }
  })
  .catch(error => console.error('Error al eliminar la película:', error));
}

// Función para abrir el formulario modal
function abrirFormulario() {
  document.getElementById("modal-form").style.display = "flex";
}

// Función para cerrar el formulario modal
function cerrarFormulario() {
  document.getElementById("modal-form").style.display = "none";
}

// Al cargar la página, cargar las películas
document.addEventListener('DOMContentLoaded', function() {
  cargarPeliculas(); // Llama a la función para cargar todas las películas
});
