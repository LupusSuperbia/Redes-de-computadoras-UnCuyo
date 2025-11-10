<?php 
define('VOTOS_DB', 'votos.txt');
define('EMAILS_DB', 'emails.txt');


if (!isset($_POST['email']) || !isset($_POST['videojuego1'])) { 
	die('Error faltan los datos del formulario'); 
}

$email_ingresado = strtolower(trim($_POST['email'])); 
$opcion_votada = $_POST['videojuego1'];

$votos = cargar_votos(VOTOS_DB);
$emails_registrados = cargar_emails(EMAILS_DB);


verificar_y_contabilizar($email_ingresado, $opcion_votada, $votos, $emails_registrados);


function verificar_y_contabilizar($email, $opcion, &$votos, &$emails_registrados){

	if (in_array($email, $emails_registrados)){
		mostrar_resultados("Usted ya votó. No puede votar dos veces", $votos, false);
		return;
	}


	// b. Contabilización del Voto (Regla b y c)
    	// Asegurarse de que la clave de la opción exista antes de incrementar
    	if (!isset($votos[$opcion])) {
        	$votos[$opcion] = 0; // Inicializar si es la primera vez
    	}
    
    	$votos[$opcion]++; // Contabilizar el voto (Regla c)

    	// Registrar el email como votado
    	$emails_registrados[] = $email;

    	// Guardar los cambios en los archivos
    	guardar_votos(VOTOS_DB, $votos);
    	guardar_emails(EMAILS_DB, $emails_registrados);
    
    	// c. Mostrar resultados
    	mostrar_resultados("¡Voto registrado con éxito!", $votos, true);
}
function cargar_votos($archivo) {
    if (!file_exists($archivo) || filesize($archivo) == 0) {
        return [];
    }
    
    $votos = [];
    $lineas = file($archivo, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    
    foreach ($lineas as $linea) {
        // Divide la línea en clave (opción) y valor (conteo)
        if (strpos($linea, '=') !== false) {
            list($opcion, $conteo) = explode('=', $linea, 2);
            $votos[trim($opcion)] = (int)trim($conteo); // Asegura que el conteo sea un número entero
        }
    }
    return $votos;
}

function guardar_votos($archivo, $votos) {
    $contenido = [];
    foreach ($votos as $opcion => $conteo) {
        $contenido[] = "{$opcion}={$conteo}"; // Formato: opcion=conteo
    }
    // Escribir todas las líneas en el archivo
    file_put_contents($archivo, implode("\n", $contenido));
    // NOTA: Recuerda que Apache (usuario 'http') debe tener permisos de escritura.
}


function cargar_emails($archivo) {
    if (!file_exists($archivo) || filesize($archivo) == 0) {
        return [];
    }
    // file() lee el archivo en un array, ignorando líneas vacías y saltos de línea al final
    return file($archivo, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
}

function guardar_emails($archivo, $emails) {
    // implode() une el array con saltos de línea.
    file_put_contents($archivo, implode("\n", $emails));
}



function mostrar_resultados($mensaje, $votos, $es_nuevo_voto) {
    echo "<h2>RESULTADOS DE LA ENCUESTA</h2>";
    echo "<p><strong>Estado:</strong> " . htmlspecialchars($mensaje) . "</p>";

    // Calcular el total de votos
    $total_votos = array_sum($votos);

    if ($total_votos == 0) {
        echo "<p>Aún no hay votos registrados.</p>";
        return;
    }
    
    echo "<h3>Estadísticas:</h3>";
    echo "<ul>";
    
    // Mostrar cada opción y su porcentaje
    foreach ($votos as $opcion => $conteo) {
        $porcentaje = ($conteo / $total_votos) * 100;
        echo "<li><strong>" . htmlspecialchars($opcion) . ":</strong> " . 
             $conteo . " votos (" . number_format($porcentaje, 2) . "%)</li>";
    }
    echo "</ul>";
    echo "<p>Total de votos en la encuesta: " . $total_votos . "</p>";
    echo "<a href='index.html'>Volver a la pagina principal</a>";
}


?>
