$(document).ready(function() {
    const urlParams = new URLSearchParams(window.location.search);
    const vistaParam = urlParams.get('vista');
    mostrarVista(vistaParam || 'historial');

    $('#selectorVista').change(function() {
        const vista = $(this).val();
        mostrarVista(vista);
    });

    inicializarEventos();
});

function mostrarVista(vista) {
    $('.vista-contenido').hide();
    
    if(vista === 'historial') {
        $('#historial-ventas').show();
    } else if(vista === 'dia') {
        $('#ventas-dia').show();
    } else if(vista === 'pedidos') {
        $('#lista-pedidos').show();
    }
    
    history.pushState(null, null, `?vista=${vista}`);
    
    inicializarEventos();
}

function inicializarEventos() {
    $('.toggle-details').off('click').on('click', function() {
        const ventaId = $(this).data('venta-id');
        $(`#detalle-${ventaId}`).toggle();
        $(this).find('i').toggleClass('bi-chevron-down bi-chevron-up');
    });

    $('.confirmar-pedido').off('click').on('click', function() {
        const $btn = $(this);
        const ventaId = $btn.data('venta-id');
        
        $.ajax({
            url: '/confirmar_pedido/' + ventaId + '/',
            method: 'POST',
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function() {
                $btn.prop('disabled', true).text('Confirmado');
                $btn.closest('tr').find('.badge')
                    .removeClass('bg-warning bg-secondary')
                    .addClass('bg-success')
                    .text('completado');
            },
            error: function() {
                alert('Error al confirmar el pedido');
            }
        });
    });

    $('#btnCorteCaja').off('click').on('click', function() {
        const ventas = [];
        let totalGeneral = 0;
        
        $("#ventas-dia tbody tr").each(function() {
            const id = $(this).find("td:eq(0)").text();
            const fecha = $(this).find("td:eq(1)").text();
            const totalText = $(this).find("td:last").text().replace("$", "").replace(",", "");
            const total = parseFloat(totalText);
            
            if (!isNaN(total)) {
                ventas.push({id, fecha, total});
                totalGeneral += total;
            }
        });
        
        $('#detalleCorte').empty();
        
        ventas.forEach(venta => {
            $('#detalleCorte').append(
                `<tr>
                    <td>${venta.id}</td>
                    <td>${venta.fecha}</td>
                    <td class="text-end">$${venta.total.toFixed(2)}</td>
                </tr>`
            );
        });
        
        $('#totalGeneralCorte').text(`$${totalGeneral.toFixed(2)}`);
        $('#corteCaja').show();
    });

    $('#btnCerrarCorte').off('click').on('click', function() {
        $('#corteCaja').hide();
    });

    $('#btnImprimirCorte').off('click').on('click', function() {
        const contenidoOriginal = $('body').html();
        const contenidoCorte = $('#corteCaja').clone();
        
        $('body').empty().append(contenidoCorte.show());
        window.print();
        $('body').html(contenidoOriginal);
        mostrarVista($('#selectorVista').val());
    });
}

/////////////

const convertirAGalletas = (cant, pres) => {
    let cantidad = pres === 'gr' ? cant / 40 : pres === 'paquete' ? cant * 6 : cant;
    return Math.floor(cantidad); 
};

const mostrarAjuste = (orig, ajust) => orig !== ajust && Swal.fire({
    title: 'Ajustando peso',
    text: `La cantidad se ha ajustado de ${orig}g a ${ajust}g`,
    icon: 'info',
    confirmButtonText: 'Entendido'
});

const ajustarGramos = (cant, pesoUnidad) => {
    const diferencia = Math.abs(cant - pesoUnidad);
    if (diferencia >= 2) {
        return Math.round(cant / pesoUnidad) * pesoUnidad;
    } else {
        return Math.floor(cant / pesoUnidad) * pesoUnidad;
    }
};

const verificarUnidades = input => {
    if ($(input).is(':focus')) return parseFloat($(input).val()) || 0;
    
    const group = $(input).closest('.galleta-group');
    const pres = group.find('[name="presentacion"]').val();
    const cant = parseFloat($(input).val()) || 0;

    if (pres === 'gr') {
        const pesoUnidad = parseFloat(group.find('[name="galletas"] option:selected').data('peso-unidad')) || 40;
        const ajustado = ajustarGramos(cant, pesoUnidad);
        if (cant !== ajustado) {
            $(input).val(ajustado);
            mostrarAjuste(cant, ajustado);
            return ajustado;
        }
    }
    return cant;
};

const calcularTotal = group => {
    const pres = group.find('[name="presentacion"]').val();
    const cant = parseFloat(group.find('[name="cantidad"]').val()) || 0;
    const precio = group.find('[name="galletas"] option:selected').data('price') || 0;
    
    if (!group.find('[name="galletas"]').val()) {
        group.find('.item-total').text('0.00');
        return;
    }

    const cantUnidades = convertirAGalletas(cant, pres);
    group.find('.item-total').text((precio * cantUnidades).toFixed(2));
    updateVentaTotal();
};

const updateVentaTotal = () => {
    let total = 0;
    $('.item-total').each((_, el) => total += parseFloat($(el).text()) || 0);
    $('#venta-total').text(total.toFixed(2));
};

const agregarProducto = () => {
    const newGroup = $(`
        <div class="galleta-group border p-3 rounded mb-3 bg-white">
            <span class="remove-galleta"><i class="bi bi-trash"></i></span>
            <div class="row">
                <div class="col-md-5 mb-3">
                    <label class="form-label fw-bold">Galleta</label>
                    <select name="galletas" class="form-select" required>
                        ${$('[name="galletas"]').first().html()}
                    </select>
                </div>
                <div class="col-md-3 mb-3">
                    <label class="form-label fw-bold">Cantidad</label>
                    <input type="number" name="cantidad" class="form-control" min="0.01" step="0.01" value="1" required>
                </div>
                <div class="col-md-3 mb-3">
                    <label class="form-label fw-bold">Presentación</label>
                    <select name="presentacion" class="form-select">
                        <option value="gr">Gramos</option>
                        <option value="unidad">Piezas</option>
                        <option value="paquete">Paquete</option>
                    </select>
                </div>
                <div class="col-md-1 mb-3 d-flex align-items-end">
                    <div class="form-control-plaintext fw-bold">$<span class="item-total">0.00</span></div>
                </div>
            </div>
            <div class="equivalencia-texto text-muted mt-2"></div>
        </div>
    `);
    
    $('#galletas-container').append(newGroup);
    $('.galleta-group .remove-galleta').not(':first').show();
    
    newGroup.find('[name="cantidad"]').off('input change').on('change', function() {
        verificarUnidades(this);
        calcularTotal(newGroup);
        actualizarEquivalencia(newGroup);
    });
    
    newGroup.find('[name="presentacion"], [name="galletas"]').on('change', function() {
        calcularTotal(newGroup);
        actualizarEquivalencia(newGroup);
    });
    
    newGroup.find('.remove-galleta').click(() => removeGalleta(newGroup));
    
    actualizarEquivalencia(newGroup);
    $('html, body').animate({scrollTop: newGroup.offset().top}, 500);
};

const removeGalleta = group => {
    if($('.galleta-group').length > 1) {
        group.remove();
        updateVentaTotal();
    }
};

$(document).ready(() => {
    $(document).on('change', '[name="cantidad"]', function() {
        verificarUnidades(this);
        calcularTotal($(this).closest('.galleta-group'));
        actualizarEquivalencia($(this).closest('.galleta-group'));
    }).on('change', '[name="presentacion"], [name="galletas"]', function() {
        calcularTotal($(this).closest('.galleta-group'));
        actualizarEquivalencia($(this).closest('.galleta-group'));
    });

    $('.galleta-group .remove-galleta').not(':first').show();
    $('[name="galletas"]').first().focus();
    
    actualizarEquivalencia($('.galleta-group').first());
});

const actualizarEquivalencia = (group) => {
    const pres = group.find('[name="presentacion"]').val();
    const cant = parseFloat(group.find('[name="cantidad"]').val()) || 0;
    const galletaSelect = group.find('[name="galletas"]');
    const galletaNombre = galletaSelect.val() ? 
        galletaSelect.find('option:selected').text().split('-')[0].trim() : '';
    const pesoUnidad = parseFloat(galletaSelect.find('option:selected').data('peso-unidad')) || 40;

    if (!galletaNombre || cant <= 0) {
        group.find('.equivalencia-texto').text('');
        return;
    }

    let unidades = convertirAGalletas(cant, pres);
    let mensaje = '';
    
    if (pres === 'gr') {
        mensaje = `${cant}g aproximadamente ${unidades} ${unidades === 1 ? 'pieza' : 'piezas'} (${pesoUnidad}g c/u)`;
    } else if (pres === 'paquete') {
        mensaje = `${cant} ${cant === 1 ? 'paquete' : 'paquetes'} son ${unidades} piezas`;
    }

    group.find('.equivalencia-texto').text(mensaje);
};
