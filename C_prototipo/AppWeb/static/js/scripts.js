// scripts.js

// Navegación a secciones de la página
document.querySelectorAll('.tab-menu a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
    });
});

// Variable para almacenar la instancia del gráfico
let chart;

// Filtrar lecturas por nombre o DNI y actualizar el gráfico
function filtrarLecturas() {
    const searchValue = document.getElementById('searchPatient').value.toLowerCase();
    const lecturasList = document.getElementById('lecturas-list');
    const ctx = document.getElementById('patientChart').getContext('2d');

    // Realizar petición al servidor para obtener lecturas filtradas
    fetch(`/api/mediciones?query=${searchValue}`)
        .then(response => response.json())
        .then(data => {
            // Limpiar lista de lecturas
            lecturasList.innerHTML = '';

            // Limpiar datos para el gráfico
            const fechas = data.map(item => item.fecha);
            const glucemia = data.map(item => item.glucemia);

            // Mostrar cada lectura en la lista
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Fecha: ${item.fecha}, Glucemia: ${item.glucemia} V`;
                lecturasList.appendChild(li);
            });

            // Destruir el gráfico anterior si existe
            if (chart) chart.destroy();

            // Crear un nuevo gráfico con los datos actualizados
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: fechas,
                    datasets: [{
                        label: 'Niveles de Glucemia',
                        data: glucemia,
                        borderColor: '#4CAF50',
                        backgroundColor: 'rgba(76, 175, 80, 0.2)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                        }
                    },
                    scales: {
                        x: { 
                            display: true, 
                            title: { display: true, text: 'Fecha' } 
                        },
                        y: { 
                            display: true, 
                            title: { display: true, text: 'Glucemia (mg/dL)' },
                            beginAtZero: true
                        }
                    }
                }
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
