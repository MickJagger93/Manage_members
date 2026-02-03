document.addEventListener('DOMContentLoaded', () => {

    // Parámetros generales
    const rowsPerPage = 10;
    let currentPage = 1;

    const table = document.getElementById('payments-table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const pagination = document.getElementById('pagination');

    // Función para filtrar filas por rangos de fecha
    function filterRows(startDate, endDate) {
        return rows.filter(row => {
            const dateCell = row.querySelector('td[data-date]');
            if (!dateCell) return false;
            const dateStr = dateCell.getAttribute('data-date');
            const rowDate = new Date(dateStr);

            if (startDate && rowDate < startDate) return false;
            if (endDate && rowDate > endDate) return false;
            return true;
        });
    }

    // Función para mostrar una página concreta
    function showPage(filteredRows, page) {
        tbody.innerHTML = '';
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const pageRows = filteredRows.slice(start, end);
        pageRows.forEach(row => tbody.appendChild(row));
        renderPagination(filteredRows.length, page);
    }

    // Función para generar botones de paginación
    function renderPagination(totalItems, page) {
        pagination.innerHTML = '';
        const totalPages = Math.ceil(totalItems / rowsPerPage);
        if (totalPages <= 1) return; // No necesario paginar

        // Botón anterior
        const prevBtn = document.createElement('button');
        prevBtn.textContent = '< Prev';
        prevBtn.disabled = page === 1;
        prevBtn.addEventListener('click', () => {
            currentPage--;
            updateDisplay();
        });
        pagination.appendChild(prevBtn);

        // Números de página
        for (let i = 1; i <= totalPages; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.textContent = i;
            pageBtn.disabled = (i === page);
            pageBtn.addEventListener('click', () => {
                currentPage = i;
                updateDisplay();
            });
            pagination.appendChild(pageBtn);
        }

        // Botón siguiente
        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Next >';
        nextBtn.disabled = page === totalPages;
        nextBtn.addEventListener('click', () => {
            currentPage++;
            updateDisplay();
        });
        pagination.appendChild(nextBtn);
    }

    // Función para actualizar la tabla y paginación de acuerdo al filtro y página actual
    function updateDisplay() {
        const startInput = document.getElementById('start-date').value;
        const endInput = document.getElementById('end-date').value;

        let startDate = startInput ? new Date(startInput) : null;
        let endDate = endInput ? new Date(endInput) : null;
        if (startDate) startDate.setHours(0,0,0,0);
        if (endDate) endDate.setHours(23,59,59,999);

        const filtered = filterRows(startDate, endDate);
        currentPage = Math.min(currentPage, Math.ceil(filtered.length / rowsPerPage) || 1);
        showPage(filtered, currentPage);
    }

    // Eventos del formulario de filtro
    const form = document.getElementById('date-filter-form');
    form.addEventListener('submit', e => {
        e.preventDefault();
        currentPage = 1;
        updateDisplay();
    });

    const clearBtn = document.getElementById('clear-filter');
    clearBtn.addEventListener('click', () => {
        document.getElementById('start-date').value = '';
        document.getElementById('end-date').value = '';
        currentPage = 1;
        updateDisplay();
    });

    // Inicializar con todos los datos
    updateDisplay();

});