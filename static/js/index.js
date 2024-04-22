$(document).ready(function(){

    $("#boton").click(function() {
        var nombre = document.getElementById('nombre').value;
        var edad = document.getElementById('edad').value;
        var ocupacion = document.getElementById('ocupacion').value;
        var direccion = document.getElementById('direccion').value;
        var correo = document.getElementById('correo').value;       
        var telefono = document.getElementById('telefono').value;
        var gato = document.getElementById('gato').value;       
        var razon = document.getElementById('razon').value;

        $.ajax({
            type: "post",
            url: "http://127.0.0.1:5000/submit",
            contentType: 'application/json',
            data: JSON.stringify({
                'nombre': nombre,
                'edad': edad,
                'ocupacion': ocupacion,
                'direccion': direccion,
                'correo': correo,
                'telefono': telefono,
                'gato': gato,
                'razon': razon,
            }),
            success: function(response) {
                alert('Data Sent: ');
            },
            error: function(xhr, status, error) {
                alert("Error: " + xhr.responseText);
            }
        });
    
        return false;
    });
});