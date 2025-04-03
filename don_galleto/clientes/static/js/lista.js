document.addEventListener("DOMContentLoaded", function () {

const loginUrl = document.body.getAttribute("data-login-url");
const isAuthenticated = document.body.getAttribute("data-is-authenticated") === "True";

  //Agregar al carrito
  document.querySelectorAll(".agregar-carrito").forEach(button => {
    button.addEventListener("click", function () {

      if (!isAuthenticated) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Debes iniciar sesión para agregar productos al carrito.',
          showConfirmButton: true,
          confirmButtonText: 'Iniciar sesión',
          confirmButtonColor: '#d33',
          allowOutsideClick: false,
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = loginUrl;
          }
        });
        return;
      }
      
      let galletaId = this.getAttribute("data-id");
      let presentacionSelect = document.getElementById(`presentacion_${galletaId}`);
      let cantidadInput = document.getElementById(`cantidad_${galletaId}`);
      let cantidad = cantidadInput ? parseInt(cantidadInput.value) : 1;
      console.log(`ID de galleta: ${galletaId}`);
      let presentacion = presentacionSelect ? presentacionSelect.value : 'Individual';
      console.log(`Presentación seleccionada: ${presentacion}`);
      
      fetch(`/clientes/agregar/${galletaId}/`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({
          cantidad: cantidad,
          presentacion: presentacion,
        })
      })
        .then(response => {
          if (!response.ok) {
            return response.json().then(data => {
              throw new Error(data.error || 'Error al agregar al carrito.');
            });
          }
          return response.json();
        })
        .then(data => {
          console.log('Respuesta del servidor:', data);
          actualizarCarrito(data.galleta); // Actualiza el carrito dinámicamente
          Swal.fire({
            icon: 'success',
            title: 'Agregado al carrito',
            text: `El producto ha sido agregado al carrito.`,
            showConfirmButton: false,
            timer: 1500
          });
        })
        .catch(error => {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.message,
            showConfirmButton: true,
          });
        });
    });
  });

  //Aumentar, disminuir y eliminar del carrito
  document.getElementById("lista-carrito").addEventListener("click", function (event) {
    let target = event.target;
    console.log('Elemento clicado',target);
    let galletaId = target.getAttribute("data-id");
    console.log(`ID de galleta: ${galletaId}`);

    if (target.classList.contains("aumentar-cantidad")) {
      actualizarCantidad(galletaId, "aumentar");
    } else if (target.classList.contains("disminuir-cantidad")) {
      actualizarCantidad(galletaId, "disminuir");
    } else if (target.classList.contains("eliminar-item")) {
      eliminarDelCarrito(galletaId);
    }
  });

  //Comprar
  document.getElementById('btn-comprar').addEventListener('click', async function () {
    const btn = this;
    window.location.href = `/clientes/detalle_compra/`;

    try {
      const items = document.querySelectorAll('.item-carrito');
      const formData = new FormData();

      items.forEach(item => {
        formData.append('galletas', item.dataset.id);
        formData.append('cantidad', item.dataset.cantidad);
        formData.append('presentacion', item.dataset.presentacion);
      });

      formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    } catch (error) {
      console.error('Error:', error);
      alert('Error al procesar la compra: ' + error.message);
      btn.disabled = false;
      btn.innerHTML = '<i class="fas fa-shopping-cart me-1"></i> Finalizar Compra';
    }
  });
});

//Abrir y cerrar carrito
document.getElementById("abrir-carrito").addEventListener("click", function () {
  document.getElementById("carrito").classList.add("mostrar");
  document.getElementById("carrito-overlay").style.display = "block";
});

document.getElementById("btn-cerrar-carrito").addEventListener("click", function () {
  document.getElementById("carrito").classList.remove("mostrar");
  document.getElementById("carrito-overlay").style.display = "none";
});

document.getElementById("carrito-overlay").addEventListener("click", function () {
  document.getElementById("carrito").classList.remove("mostrar");
  this.style.display = "none";
});

//Actualizar cantidad de galletas en el carrito
function actualizarCantidad(galletaId, accion) {
  fetch(`/clientes/actualizar/${galletaId}/`, {
    method: "POST",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie('csrftoken')
    },
    body: JSON.stringify({
      accion: accion
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Respuesta del servidor:', data); // 👀 Verificar si el subtotal llega correcto
      if (data.success) {
        actualizarCarrito(data.galleta);
      } else {
        console.error('Error al actualizar la cantidad:', data.error);
      }
    })
    .catch(error => console.error("Error al actualizar la cantidad:", error));
}

//Eliminar producto del carrito
function eliminarDelCarrito(galletaId) {
  console.log(`Eliminando galleta con ID: ${galletaId}`);

  fetch(`/clientes/eliminar/${galletaId}/`, {
    method: "POST",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie('csrftoken')
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Respuesta del servidor:', data);
      if (data.success) {
        // Actualiza el carrito completo en el DOM
        actualizarCarrito(data.carrito);

        Swal.fire({
          icon: 'success',
          title: 'Eliminado',
          text: `La galleta ha sido eliminada del carrito.`,
          showConfirmButton: false,
          timer: 1500
        });

        // Actualiza el total en el DOM
        document.getElementById('total-carrito').textContent = `Total: $${data.total.toFixed(2)}`;
      } else {
        console.error('Error al eliminar el producto:', data.message);
      }
    })
    .catch(error => console.error("Error al eliminar el producto:", error));
}

//Obtener el valor de una cookie por su nombre
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

//Actualizar el carrito en la interfaz
function actualizarCarrito(carrito) {
  let listaCarrito = document.getElementById("lista-carrito");
  let totalCarrito = document.getElementById("total-carrito");
  listaCarrito.innerHTML = ""; // Limpia el contenido actual del carrito
  let total = 0;

  if (!carrito || Object.keys(carrito).length === 0) {
    listaCarrito.innerHTML = "<li class='list-group-item'>El carrito está vacío</li>";
    totalCarrito.textContent = "Total: $0.00";
    return;
  }

  Object.values(carrito).forEach((item, index) => {
    let li = document.createElement("li");
    li.className = "item-carrito";
    li.dataset.id = item.id_galleta; 
    li.innerHTML = `
      <span>${item.nombre} 
      <br>$${item.precio_venta} 
      <br>Cantidad: ${item.cantidad} pieza(s)</span>
      <br><span>Subtotal: $${item.subtotal.toFixed(2)}</span>
      <button class="btn btn-danger btn-sm eliminar-item" data-id="${item.id_galleta}">Eliminar</button>
    `;
    li.style.animationDelay = `${index * 0.1}s`;
    listaCarrito.appendChild(li);
    total += item.subtotal;
  });

  totalCarrito.textContent = `Total: $${total.toFixed(2)}`;
}

//Prueba para hacer push

  function validarCantidad(input) {
    if (input.value < 1) {
      input.value = 1; 
    }
  }

  document.getElementById('btn-comprar').addEventListener('click', function (event) {
    const listaCarrito = document.getElementById("lista-carrito");
  
    // Verifica si el carrito está vacío
    if (!listaCarrito.children.length || listaCarrito.innerHTML.includes("El carrito está vacío")) {
      event.preventDefault(); // Evita la acción predeterminada del botón
      Swal.fire({
        icon: 'error',
        title: 'Carrito vacío',
        text: 'No puedes realizar una compra sin productos en el carrito.',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#d33',
      });
      return;
    }
  
    window.location.href = `/clientes/detalle_compra/`;
  });

