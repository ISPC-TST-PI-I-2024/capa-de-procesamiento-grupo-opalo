// scripts.js

// Navegación a secciones de la página
document.querySelectorAll('.tab-menu a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
    });
});

// Filtrar lecturas por nombre o DNI
function filtrarLecturas() {
    const searchValue = document.getElementById('searchPatient').value.toLowerCase();
    const lecturasList = document.getElementById('lecturas-list');
    
    // Realizar petición al servidor para obtener lecturas filtradas
    fetch(`/api/mediciones?query=${searchValue}`)
        .then(response => response.json())
        .then(data => {
            lecturasList.innerHTML = '';
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Fecha: ${item.fecha}, Glucemia: ${item.glucemia} V`;
                lecturasList.appendChild(li);
            });
        })
        .catch(error => console.error('Error al filtrar lecturas:', error));
}

// Mostrar detalles de un paciente al seleccionar
function mostrarDetallesPaciente(paciente_id) {
    const detallesDiv = document.getElementById('paciente-detalles');
    
    // Realizar petición al servidor para obtener detalles del paciente
    fetch(`/api/pacientes/${paciente_id}`)
        .then(response => response.json())
        .then(data => {
            detallesDiv.innerHTML = `
                <h3>Datos Personales</h3>
                <p>Nombre: ${data.nombre}</p>
                <p>Apellido: ${data.apellido}</p>
                <p>Fecha de Nacimiento: ${data.fecha_nacimiento}</p>
                <p>Sexo: ${data.sexo}</p>
                <p>Dirección: ${data.direccion}</p>
                <p>Peso: ${data.peso} kg</p>
                <p>Altura: ${data.altura} cm</p>
                <h3>Contacto de Emergencia</h3>
                <p>Nombre: ${data.contacto.nombre}</p>
                <p>Teléfono: ${data.contacto.telefono}</p>
                <p>Parentesco: ${data.contacto.parentesco}</p>
            `;
        })
        .catch(error => console.error('Error al obtener detalles del paciente:', error));
}
