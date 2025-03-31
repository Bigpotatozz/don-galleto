document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".agregar-carrito").forEach(button => {
      button.addEventListener("click", function () {
        let galletaId = this.getAttribute("data-id");
        let presentacionSelect = document.getElementById(`presentacion_${galletaId}`);
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
            presentacion: presentacion
          })
        })
          .then(response => response.json())
          .then(data => {
            console.log('Respuesta del servidor:', data);
            actualizarCarrito(data.galleta);
            Swal.fire({
              icon: 'success',
              title: 'Agregado al carrito',
              text: `La galleta ha sido agregado al carrito.`,
              showConfirmButton: false,
              timer: 1500
            });
            this.innerHTML = '<i class="fas fa-check"></i>';
          })
          .catch(error => console.error("Error al agregar al carrito:", error));
      });
    });

    document.getElementById('btn-comprar').addEventListener('click', async function () {
      const btn = this;

      window.location.href = `/clientes/detalle_compra/`;

      btn.disabled = true;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Procesando...';

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

  function actualizarCarrito(carrito) {
    let listaCarrito = document.getElementById("lista-carrito");
    let totalCarrito = document.getElementById("total-carrito");
    listaCarrito.innerHTML = "";
    let total = 0;
    carrito.forEach((item, index) => {
      let li = document.createElement("li");
      li.textContent = `${item.nombre} - $${item.precio_venta} (x${item.cantidad})`;
      li.style.animationDelay = `${index * 0.1}s`;
      listaCarrito.appendChild(li);
      total += item.precio_venta * item.cantidad;
    });
    totalCarrito.textContent = `Total: $${total.toFixed(2)}`;
  }

  document.getElementById("abrir-carrito").addEventListener("click", function () {
    document.getElementById("carrito").classList.add("mostrar");
  });

  document.getElementById("btn-cerrar-carrito").addEventListener("click", function () {
    document.getElementById("carrito").classList.remove("mostrar");
  });

  document.querySelectorAll(".btn-incrementar").forEach(button => {
    button.addEventListener("click", function () {
      let input = this.previousElementSibling;
      input.value = parseInt(input.value) + 1;
    });
  });

  document.querySelectorAll(".btn-decrementar").forEach(button => {
    button.addEventListener("click", function () {
      let input = this.nextElementSibling;
      if (parseInt(input.value) > 1) {
        input.value = parseInt(input.value) - 1;
      }
    });
  });
