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


    const alertContainer = document.querySelector(".alert-container");
    if (alertContainer) {
      const alertMessage = alertContainer.querySelector(".alert").textContent.trim();
      const alertType = alertContainer.querySelector(".alert").classList.contains("alert-success") ? "success" : "error";

      Swal.fire({
        title: alertType === "success" ? "¡Éxito!" : "Error",
        text: alertMessage,
        icon: alertType,
        confirmButtonText: "Aceptar",
        confirmButtonColor: "#27ae60",
      });
    }

  });