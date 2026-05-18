document.addEventListener("DOMContentLoaded", () => {
    const zoomGuardado = localStorage.getItem("sares-zoom");
    if (zoomGuardado) {
        aplicarZoom(zoomGuardado);
    }
});

function cambiarTexto(factor) {
    // El zoom por defecto o base es 1 (100%)
    let zoomActual = parseFloat(localStorage.getItem("sares-zoom")) || 1.0;
    
    // Si factor es 2, sumamos 0.15 (sube tamaño). Si es -2, restamos 0.15 (baja tamaño)
    let modificador = factor > 0 ? 0.15 : -0.15;
    let nuevoZoom = zoomActual + modificador;
    
    // Límites de seguridad para que no se vuelva gigante ni diminuto (entre 70% y 160%)
    if (nuevoZoom >= 0.7 && nuevoZoom <= 1.6) {
        aplicarZoom(nuevoZoom);
        localStorage.setItem("sares-zoom", nuevoZoom);
    }
}

function aplicarZoom(nivelZoom) {
    let estiloAccesibilidad = document.getElementById("estilo-accesibilidad");
    
    if (!estiloAccesibilidad) {
        estiloAccesibilidad = document.createElement("style");
        estiloAccesibilidad.id = "estilo-accesibilidad";
        document.head.appendChild(estiloAccesibilidad);
    }
    
    // ¡Aquí está el truco de ingeniería! Usamos la propiedad zoom en la raíz html.
    // Esto escala de forma perfecta e idéntica toda la pantalla manteniendo las 
    // proporciones originales de los títulos, botones y cajas de texto.
    estiloAccesibilidad.innerHTML = `
        html { 
            zoom: ${nivelZoom} !important; 
            -moz-transform: scale(${nivelZoom}); 
            -moz-transform-origin: top center;
        }
    `;
}