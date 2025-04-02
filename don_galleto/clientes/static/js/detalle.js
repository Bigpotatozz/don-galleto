document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn-incrementar").forEach(button => {
      button.addEventListener("click", function () {
        let input = this.previousElementSibling;
        input.value = parseInt(input.value) + 1;
        actualizarTotal(this.dataset.id, input.value);
      });
    });

    document.querySelectorAll(".btn-decrementar").forEach(button => {
      button.addEventListener("click", function () {
        let input = this.nextElementSibling;
        if (parseInt(input.value) > 1) {
          input.value = parseInt(input.value) - 1;
          actualizarTotal(this.dataset.id, input.value);
        }
      });
    });

    function actualizarTotal(id, cantidad) {
      const precio = parseFloat(document.querySelector(`[data-id="${id}"]`).dataset.precio);
      const totalProducto = precio * cantidad;
      document.querySelector(`#total-producto-${id}`).textContent = `Total por producto: $${totalProducto.toFixed(2)}`;
    }
  });