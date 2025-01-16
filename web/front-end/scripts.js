function registrarUsuario() {
  document.getElementsByClassName("error")[0].style.display = "none";

  var raw = JSON.stringify({
    nombre: document.getElementById("nombre").value,
    email: document.getElementById("email").value,
    contrasena: document.getElementById("password").value,
    logeado: false,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
  };

  fetch("/registro", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status === "OK") {
        mostrarModal();
      } else {
        document.getElementsByClassName("error")[0].style.display = "block";
      }
    })
    .catch((error) => console.log("error", error));
}

function mostrarModal() {
  const modal = document.getElementById("successModal");
  modal.style.display = "flex";
}

function cerrarModal() {
  const modal = document.getElementById("successModal");
  modal.style.display = "none";
  location.href = "views/login/login.html";
}
