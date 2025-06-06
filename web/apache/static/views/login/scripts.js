var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

function iniciarSesion() {
  document.getElementsByClassName("error")[0].style.display = "none";
  var raw = JSON.stringify({
    email: document.getElementById("email").value,
    contrasena: document.getElementById("password").value,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
  };

  fetch("/api/login", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status == "OK") {
        alert("Usuario logeado correctamente");
        location.href = "../home/home.html";
      } else {
        document.getElementsByClassName("error")[0].style.display = "block";
      }
    })
    .catch((error) => console.log("error", error));
}
