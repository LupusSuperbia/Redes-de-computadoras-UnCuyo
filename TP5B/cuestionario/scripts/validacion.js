function validar() {
	var email_ingresado = document.getElementById("email_id").value;
	if(email_ingresado.length == 0){ 
		return alert("Porfavor ingrese un mail")
	}

	if(!(verificarEmail(email_ingresado))){
		return ; 
	}
	var opciones = document.getElementById("cuestionario");
	if(!verificarOpcionSeleccionada(opciones)){ 
		alert("Por favor seleccione una opcion")
	}
	console.log(email_ingresado)
}


function verificarOpcionSeleccionada(opciones) {
    if (opciones.length === 0) {
        return false;
    }
    
    for (let i = 0; i < opciones.length; i++) {
        if (opciones[i].checked) {
            
            return true;
        }
    }
    // Ninguna opción seleccionada
    return false;
}




function verificarEmail(email){
	const regexEmailSeguro = /^(?!.*[#!%$])([^@\.]+)@([^@\.]+)\.([^@\.]+)$/;
	console.log(email.length)
	if(email.length < 7){ 
		alert("El mail debe poseer como minimo 7 caracteres");
		return true;
	}
	if(regexEmailSeguro.test(email)){
		console.log("La cadena cumple con todos los requisitos");
		return true; 
	}
	else { 
		alert("La cadena no cumple con los requisitos, verifique el email ingresado");
		return false;
	}

}
