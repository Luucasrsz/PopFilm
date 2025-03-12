function checkLogin() {
    // Verificar si el token JWT está presente en las cookies
    const token = getCookie("access_token_cookie");
  
    if (!token) {
      alert("Por favor, inicia sesión para acceder.");
      location.href = "/login/login.html";
    } else {
      // Si hay un token, se puede verificar con el backend si es válido
      fetch("/api/protegido", {
        method: "GET",
        headers: {
          "Authorization": "Bearer " + token
        }
      })
        .then((response) => {
          if (response.status !== 200) {
            alert("El token no es válido o ha expirado. Por favor, inicia sesión nuevamente.");
            location.href = "/login/login.html";  // Redirige al login si el token no es válido
          }
        })
        .catch((error) => {
          console.error("Error al verificar el token:", error);
          alert("Ocurrió un error al verificar la sesión.");
          location.href = "/login/login.html";  // Redirige al login en caso de error
        });
    }
  }
  
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
  