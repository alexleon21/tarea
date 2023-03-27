document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('form');
  const btnGenerar = document.getElementById('btnGenerar');
  const btnGrabar = document.getElementById('btnGrabar');
  const idCuota = document.getElementById('idCuota');
  const detalle = document.getElementById('detalle');
  const btnPago = document.getElementById('btnPago');
  const cboFecha = document.getElementById('cboFecha');

  function calcularCuotaSaldo() {
    const credito = parseFloat(form.credito.value);
    const numeroPagos = parseInt(form.numero_pagos.value);

    if (credito && numeroPagos) {
      const cuota = credito / numeroPagos;
      form.cuota.value = cuota.toFixed(2);
      form.saldo.value = credito.toFixed(2);
    } else {
      form.cuota.value = '';
      form.saldo.value = '';
    }
  }

  function generarPagos() {
    const numeroPagos = parseInt(form.numero_pagos.value);
    const cuota = parseFloat(form.cuota.value);
    const fechaPrimerPago = new Date(form.fecha_primer_pago.value);

    detalle.innerHTML = '';

    for (let i = 0; i < numeroPagos; i++) {
      const fechaPago = new Date(fechaPrimerPago);
      fechaPago.setDate(fechaPago.getDate() + i * 30);

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${i + 1}</td>
        <td>${fechaPago.toLocaleDateString('es-ES')}</td>
        <td>${cuota.toFixed(2)}</td>
        <td>Pendiente</td>
        <td class="text-center text-danger">
          <input type="checkbox" data-index="${i}" class="chkPagar">
        </td>
      `;

      detalle.appendChild(tr);
    }
  }

  function agregarPago() {
    const index = parseInt(cboFecha.value);
    const cuota = parseFloat(idCuota.value);
    const pagado = document.querySelector(`.chkPagar[data-index="${index}"]`).checked;
    const estado = pagado ? 'Pagado' : 'Pendiente';
  
    const tr = detalle.querySelector(`tr[data-index="${index}"]`);
    if (tr) {
      tr.querySelector('td:nth-child(3)').textContent = cuota.toFixed(2);
      tr.querySelector('td:nth-child(4)').textContent = estado;
      tr.querySelector('.chkPagar').checked = pagado;
  
      // cambiar estado a Pendiente si se desmarca el checkbox de pago
      if (!pagado) {
        tr.querySelector('td:nth-child(4)').textContent = 'Pendiente';
        tr.querySelector('.chkPagar').checked = false;
      }
  
      // Actualizar el atributo 'data-estado' del elemento 'tr'
      tr.dataset.estado = pagado ? '1' : '0';
    }
  }

  function validarDatos() {
    return form.fecha_credito.value && form.credito.value && form.cliente.value && form.numero_pagos.value && form.cuota.value && form.fecha_primer_pago.value && form.saldo.value && form.motivo.value;
  }

  form.addEventListener('input', calcularCuotaSaldo);
  btnGenerar.addEventListener('click', generarPagos);
  btnPago.addEventListener('click', agregarPago);

  btnGrabar.addEventListener('click', function (event) {
    event.preventDefault();
    if (validarDatos()) {
      const request = new Request(crear_cuenta_url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify({
          fecha_credito: form.fecha_credito.value,
          credito: form.credito.value,
          cliente: form.cliente.value,
          numero_pagos: form.numero_pagos.value,
          cuota: form.cuota.value,
          fecha_primer_pago: form.fecha_primer_pago.value,
          saldo: form.saldo.value,
          motivo: form.motivo.value,
          pagos: Array.from(detalle.querySelectorAll('tr')).map(tr => ({
            fecha_pago: tr.querySelector('td:nth-child(2)').textContent,
            cuota: parseFloat(tr.querySelector('td:nth-child(3)').textContent),
            pagado: tr.querySelector('.chkPagar').checked,
          })),
        }),
      });

      if (request.headers.get('X-Requested-With') !== 'XMLHttpRequest') {
        request.headers.append('X-Requested-With', 'XMLHttpRequest');
      }

      fetch(request)
        .then(response => {
          if (response.ok) {
            response.json().then(data => {
              if (data.status === 'success') {
                alert('El registro se guardó correctamente');
                window.location.href = "/cuenta/";
              } else {
                alert('Ocurrió un error al guardar el registro');
              }
            }).catch(error => {
              alert('La respuesta recibida no es un JSON válido: ' + error.message);
            });
          } else {
            response.text().then(text => {
              alert('Error al guardar el registro: ' + response.statusText + ', ' + text);
            });
          }
        });
    } else {
      alert('Por favor, complete todos los campos obligatorios');
    }
  });

  document.querySelectorAll('.estado-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
      const row = this.closest('tr');
      const estado = this.checked ? 'Pagado' : 'Pendiente';
      row.querySelector('td:nth-child(4)').textContent = estado;
      row.querySelector('input[type="hidden"]').value = `${row.dataset.id},${this.checked ? '1' : '0'}`;
    });
  });
});