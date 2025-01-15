var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

function iniciarSesion() {
  document.getElementsByClassName("error")[0].style.display = "none";
  var raw = JSON.stringify({
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
  };

  fetch("/login", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      if (result.status == "OK") {
        alert("Usuario registrado correctamente");
        location.href = "../control-panel/control.html";
      } else {
        document.getElementsByClassName("error")[0].style.display = "block";
      }
    })
    .catch((error) => console.log("error", error));
}
