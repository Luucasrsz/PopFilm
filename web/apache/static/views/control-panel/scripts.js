var myHeaders = new Headers();
let modoEdicion = false; // Variable que indicará si estamos en modo edición
let idPeliculaEditando = null; // Almacenará el ID de la película que estamos editando

onload = () => {
  if (!sessionStorage.getItem("perfil") || sessionStorage.getItem("perfil") == "normal") {
    location.href = "../home/home.html";
  } else {
    myHeaders.append("Content-Type", "application/json");
    if (sessionStorage.getItem("csrf_token")) {
      myHeaders.append("X-CSRFToken", sessionStorage.getItem("csrf_token"));
    }
  }
};

// Función para editar una película
function editarPelicula(id) {
  idPeliculaEditando = id; // Guardamos el ID de la película que estamos editando
  modoEdicion = true; // Activamos el modo de edición

  fetch(`/api/pelicula/${id}`, {
    method: "GET",
    headers: myHeaders,
  })
    .then((response) => response.json())
    .then((pelicula) => {
      document.getElementById("titulo").value = pelicula.nombre;
      document.getElementById("sinopsis").value = pelicula.sinopsis;
      document.getElementById("categoria").value = pelicula.categoria;
      document.getElementById("precio").value = pelicula.precio;

      // Cambiar el evento del formulario a 'guardarCambios' (PUT)
      abrirFormulario(); // Mostrar el formulario modal
    })
    .catch((error) => {
      console.error("Error al obtener los detalles de la película:", error);
    });
}

// Función para guardar o actualizar la película
function guardarCambios(event) {
  event.preventDefault(); // Evitar la acción por defecto del formulario

  const nombre = document.getElementById("titulo").value;
  const sinopsis = document.getElementById("sinopsis").value;
  const categoria = document.getElementById("categoria").value;
  const precio = parseFloat(document.getElementById("precio").value);

  let datos = JSON.stringify({
    nombre,
    sinopsis,
    categoria,
    precio,
  });

  let requestOptions = {
    method: modoEdicion ? "PUT" : "POST", // Usar PUT si estamos editando, POST si estamos creando
    headers: myHeaders,
    body: datos,
  };

  // Si estamos editando, usamos PUT y la URL debe incluir el ID
  const url = modoEdicion ? `/api/peliculas/${idPeliculaEditando}` : `/api/peliculas/insertar`;

  fetch(url, requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status === "OK") {
        alert(modoEdicion ? "Película editada" : "Película guardada");
        cerrarFormulario();
        cargarPeliculas();
      } else {
        alert("Error al guardar la película");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Se ha producido un error y la película no ha podido ser guardada");
    });
}

// Función para abrir el formulario modal
function abrirFormulario() {
  document.getElementById("modal-form").style.display = "flex";
}

// Función para cerrar el formulario modal
function cerrarFormulario() {
  document.getElementById("modal-form").style.display = "none";
  modoEdicion = false; // Resetear el modoEdicion al cerrar el formulario
  idPeliculaEditando = null; // Limpiar el ID de la película
}

// Función para cargar todas las películas
function cargarPeliculas() {
  fetch(`/api/peliculas`, {
    method: "GET",
    headers: myHeaders,
  })
    .then((response) => response.json())
    .then((peliculas) => {
      const tableBody = document.getElementById("movie-list");
      tableBody.innerHTML = "";
      peliculas.forEach((pelicula) => {
        agregarFila(
          pelicula.nombre,
          pelicula.categoria,
          pelicula.sinopsis,
          pelicula.precio,
          pelicula.id
        );
      });
    })
    .catch((error) => console.error("Error al cargar las películas:", error));
}

// Función para agregar una fila a la tabla de películas
function agregarFila(nombre, categoria, sinopsis, precio, id) {
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
  const tdAcciones = document.createElement("td");

  // Botón de editar
  const btnEditar = document.createElement("button");
  btnEditar.textContent = "Editar";
  btnEditar.onclick = function () {
    editarPelicula(id); // Llamar a la función de editar con el ID de la película
  };

  // Botón de eliminar
  const btnEliminar = document.createElement("button");
  btnEliminar.textContent = "Eliminar";
  btnEliminar.addEventListener("click", function () {
    eliminarPelicula(id);
  });

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
  row.appendChild(tdAcciones);

  tableBody.appendChild(row);
}

// Función para eliminar una película
function eliminarPelicula(id) {
  fetch(`/api/peliculas/${id}`, {
    method: "DELETE",
    headers: myHeaders,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "OK") {
        alert("Película eliminada");
        cargarPeliculas(); // Recargar la lista de películas
      } else {
        alert("Error al eliminar la película");
      }
    })
    .catch((error) => console.error("Error al eliminar la película:", error));
}

// Al cargar la página, cargar las películas
document.addEventListener("DOMContentLoaded", function () {
  cargarPeliculas(); // Llama a la función para cargar todas las películas
  
  // Usamos solo un único 'submit' handler para guardar la película
  document.getElementById("movie-form").addEventListener("submit", guardarCambios);
});

function calcularIVA(precio) {
  return precio * 0.21;
}
