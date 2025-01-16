var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

function registrarUsuario() {
  document.getElementsByClassName("error")[0].style.display = "none";
  var raw = JSON.stringify({
    nombre: document.getElementById("nombre").value,
    email: document.getElementById("email").value,
    contrasena: document.getElementById("password").value,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
  };

  fetch("/registro", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status == "OK") {
        alert("Usuario registrado correctamente");
        location.href = "views/home/home.html";
      } else {
        document.getElementsByClassName("error")[0].style.display = "block";
      }
    })
    .catch((error) => console.log("error", error));
}
