var myHeaders = new Headers();

document.addEventListener('DOMContentLoaded', function() {
  if (!sessionStorage.getItem("csrf_token")) {
    window.location.href = "../../index.html";
  } else {
    cargarPeliculas();
  }
});


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
function guardarCambios(event) {
  event.preventDefault();

  const nombre = document.getElementById("titulo").value;
  const sinopsis = document.getElementById("sinopsis").value;
  const categoria = document.getElementById("categoria").value;
  const precio = parseFloat(document.getElementById("precio").value);
  const portada = document.getElementById("portada").files[0]; 

  const formData = new FormData();
  formData.append("id", peliculaId); 
  formData.append("nombre", nombre);
  formData.append("sinopsis", sinopsis);
  formData.append("categoria", categoria);
  formData.append("precio", precio);

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
        cargarPeliculas();
      } else {
        alert(`Hubo un error al actualizar la película: ${result.message || "Error desconocido"}`);
      }
    })
    .catch(error => {
      console.error('Error al actualizar la película:', error);
      alert(`Se ha producido un error: ${error.message || "Error desconocido"}`);
    });
}



// Función para calcular el IVA
function calcularIVA(precio) {
  return precio * 0.21;
}

// Función para agregar una fila a la tabla de películas
function agregarFila(nombre, categoria, sinopsis, precio, portada, id) {
  const tableBody = document.getElementById("movie-list");

  const row = document.createElement("tr");

  const tdNombre = document.createElement("td");
  tdNombre.textContent = nombre;
  const tdCategoria = document.createElement("td");
  tdCategoria.textContent = categoria;
  const tdSinopsis = document.createElement("td");
  tdSinopsis.textContent = sinopsis;
  const tdPrecio = document.createElement("td");
  tdPrecio.textContent = precio;
  const tdPortada = document.createElement("td");
  tdPortada.textContent = portada;
  const tdAcciones = document.createElement("td");

  // Botón de editar
  const btnEditar = document.createElement("button");
  btnEditar.textContent = "Editar";
  btnEditar.onclick = function() {
      editarPelicula(id);
  };

  // Botón de eliminar
  const btnEliminar = document.createElement("button");
  btnEliminar.textContent = "Eliminar";
  btnEliminar.addEventListener("click", function() {
      eliminarPelicula(id);
  });

  // Botón de calcular IVA
  const btnCalcularIVA = document.createElement("button");
  btnCalcularIVA.textContent = "Calcular IVA";
  btnCalcularIVA.onclick = function() {
      alert(`El IVA de ${nombre} es: $${calcularIVA(precio).toFixed(2)}`);
  };

  tdAcciones.appendChild(btnEditar);
  tdAcciones.appendChild(btnEliminar);
  tdAcciones.appendChild(btnCalcularIVA);

  row.appendChild(tdNombre);
  row.appendChild(tdCategoria);
  row.appendChild(tdSinopsis);
  row.appendChild(tdPrecio);
  row.appendChild(tdPortada);
  row.appendChild(tdAcciones);

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
