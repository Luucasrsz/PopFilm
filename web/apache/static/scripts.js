var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        function registrarUsuario(){
            document.getElementsByClassName("error")[0].style.display="none";
            var raw = JSON.stringify({
                "usuario": document.getElementById("usuario").value,
                "contrasena": document.getElementById("contrasena").value,
                "email": document.getElementById("email").value,
                "perfil": "normal"
            });
            console.log(raw)

            var requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: raw
            };

            console.log(requestOptions)

            fetch("/api/registro", requestOptions)
                .then(response => response.json())
                .then(result => {
                    if (result.status=="OK"){
                        alert("Usuario registrado correctamente");
                        location.href="index.html";
                    } else {
                        document.getElementsByClassName("error")[0].style.display="block";
                    }
                })
                .catch(error => console.log('error', error)); 
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

