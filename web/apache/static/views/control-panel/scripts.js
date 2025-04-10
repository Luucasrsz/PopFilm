var myHeaders = new Headers();
onload=()=>{
    if (!sessionStorage.getItem("perfil") || sessionStorage.getItem("perfil")=="normal"){
        location.href="../home/home.html"
    } else {
        myHeaders.append("Content-Type", "application/json");
        if (sessionStorage.getItem("csrf_token")){
            myHeaders.append("X-CSRFToken",sessionStorage.getItem("csrf_token"))
        }
    }
}

// URL base de la API
const apiUrl = "/api/peliculas"; // Ajustar según la URL de tu API
// Función para editar una película
let peliculaId; // Variable global para almacenar el ID de la película

// Función para editar una película
function editarPelicula(id) {
  peliculaId = id; // Almacenar el ID al editar la película
  fetch(`/api/pelicula/${id}`, {
    method: "GET",
    headers: myHeaders
  })
    .then((response) => response.json())
    .then((pelicula) => {
      console.log(pelicula.nombre);
      // Rellenar los campos del formulario con los datos actuales de la película
      document.getElementById("titulo").value = pelicula.nombre;
      document.getElementById("sinopsis").value = pelicula.sinopsis;
      document.getElementById("categoria").value = pelicula.categoria;
      document.getElementById("precio").value = pelicula.precio;

      // Cambiar la función del formulario a guardarCambios
      document.getElementById("movie-form").onsubmit = guardarCambios;

      // Abrir el formulario modal
      abrirFormulario();
    })
    .catch((error) => {
      console.error("Error al obtener los detalles de la película:", error);
    });
}

function guardarCambios() {
  const nombre = document.getElementById("titulo").value;
  const sinopsis = document.getElementById("sinopsis").value;
  const categoria = document.getElementById("categoria").value;
  const precio = parseFloat(document.getElementById("precio").value);

  let datos = JSON.stringify({
    "id": id,
    "nombre": nombre,
    "sinopsis": sinopsis,
    "categoria": categoria,
    "precio": precio,
  });


  let requestOptions = {
    method: "PUT",
    headers: myHeaders,
    body: datos,
  };

  fetch(`/api/peliculas/editar`, requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status == "OK") {
        alert("Pelicula editada");
        cerrarFormulario();
        cargarPeliculas();
      } else {
        alert("La pelicula no ha podido ser editada");
      }
    })
    .catch((error) => {
      console.log("error", error);
      alert("Se ha producido un error y la chuche no ha podido ser guardado");
    });
}

// Función para guardar los cambios de una película
function insertMovie() {
  const nombre = document.getElementById("titulo").value;
  const sinopsis = document.getElementById("sinopsis").value;
  const categoria = document.getElementById("categoria").value;
  const precio = parseFloat(document.getElementById("precio").value);

  let datos = JSON.stringify({
    "nombre": nombre,
    "sinopsis": sinopsis,
    "categoria": categoria,
    "precio": precio,
  });
  let requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: datos,
  };

  fetch(`/api/peliculas/insertar`, requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status == "OK") {
        alert("Pelicula guardada");
        cerrarFormulario();
        cargarPeliculas();
      } else {
        alert("La pelicula no ha podido ser guardado");
      }
      console.log("lucas tonto")
    })
    .catch((error) => {
      console.log("error", error);
      alert("Se ha producido un error y la pelicula no ha podido ser guardado");
    });
}
// Función para calcular el IVA
function calcularIVA(precio) {
  return precio * 0.21;
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
    editarPelicula(id);
  };

  // Botón de eliminar
  const btnEliminar = document.createElement("button");
  btnEliminar.textContent = "Eliminar";
  btnEliminar.addEventListener("click", function () {
    eliminarPelicula(id);
  });

  // Botón de calcular IVA
  const btnCalcularIVA = document.createElement("button");
  btnCalcularIVA.textContent = "Calcular IVA";
  btnCalcularIVA.onclick = function () {
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

// Función para cargar todas las películas
function cargarPeliculas() {
  fetch(`/api/peliculas`, {
    method: "GET",
    headers: myHeaders
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

// Función para eliminar una película
function eliminarPelicula(id) {
  console.log("ELIMINAR");
  console.log(id);
  fetch(`/api/peliculas/${id}`, {
    method: "DELETE",
    headers: myHeaders
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

// Función para abrir el formulario modal
function abrirFormulario() {
  document.getElementById("modal-form").style.display = "flex";
}

// Función para cerrar el formulario modal
function cerrarFormulario() {
  document.getElementById("modal-form").style.display = "none";
}

// Al cargar la página, cargar las películas
document.addEventListener("DOMContentLoaded", function () {
  cargarPeliculas(); // Llama a la función para cargar todas las películas
});