import io from 'socket.io-client';

const socket = io('http://127.0.0.1:8000');

// Escuchar eventos del backend
socket.on('evento', data => {
  // Hacer algo con los datos recibidos del backend
});

// Enviar datos al backend
socket.emit('evento', { ... });


function getItems() {
    fetch('http://127.0.0.1:8000/Items ')  // Hacer una solicitud GET al endpoint '/items' del backend
        .then(response => response.json())  // Convertir la respuesta en formato JSON
        .then(data => {
            const itemList = document.getElementById('itemList');

            // Limpiar la lista antes de agregar nuevos elementos
            itemList.innerHTML = '';

            // Iterar los elementos recibidos y agregarlos a la lista
            data.items.forEach(item => {
                const li = document.createElement('li');
                li.innerText = `ID: ${item.id}, Nombre: ${item.name}`;
                itemList.appendChild(li);
            });
        })
        .catch(error => console.error('Error al obtener elementos:', error));
}
