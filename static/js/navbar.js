document.addEventListener("DOMContentLoaded", function() {
    var navbarIframe = document.getElementById("header");

    navbarIframe.addEventListener("load", function() {
        var navbarLinks = navbarIframe.contentDocument.querySelectorAll("a");

        navbarLinks.forEach(function(link) {
            link.addEventListener("click", function(event) {
                // Verificar si el clic se realizó en un ícono o en una imagen dentro del enlace
                if (event.target.tagName.toLowerCase() === 'i' || event.target.tagName.toLowerCase() === 'img') {
                    // Obtener la URL del enlace desde el atributo "href" del elemento padre (el <a>)
                    var href = event.target.parentNode.getAttribute("href");
                    window.top.location.href = href; // Redireccionar la página principal a la URL del enlace
                } else {
                    // Prevenir el comportamiento predeterminado del enlace
                    event.preventDefault();
                    // Obtener la URL del enlace desde el atributo "href" del elemento <a>
                    var href = event.target.getAttribute("href");
                    window.top.location.href = href; // Redireccionar la página principal a la URL del enlace
                }
            });
        });
    });
});