/**
 * Grid.js utilities for Buffet San Patricio.
 * Provides reusable functions for data tables with GridJS.
 */

const GridUtils = window.GridUtils || {};

/**
 * Show loading spinner in container.
 */
GridUtils.showLoading = function(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `
        <div class="d-flex justify-content-center align-items-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <span class="ms-2 text-muted">Cargando datos...</span>
        </div>
    `;
};

/**
 * Show error message in container.
 */
GridUtils.showError = function(containerId, message) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `
        <div class="alert alert-danger d-flex align-items-center" role="alert">
            <span class="material-icons me-2">error</span>
            <div>${message}</div>
        </div>
    `;
};

/**
 * Get data from currently rendered GridJS table.
 * @returns {Array} Array of row data arrays
 */
GridUtils.getTableData = function() {
    const table = document.querySelector('.gridjs-table');
    if (!table) return [];

    const rows = [];
    const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
    rows.push(headers);

    table.querySelectorAll('tbody tr').forEach(tr => {
        const row = Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim());
        rows.push(row);
    });

    return rows;
};

/**
 * Copy GridJS table data to clipboard.
 */
GridUtils.copyToClipboard = function() {
    const table = document.querySelector('.gridjs-table');
    if (!table) {
        alert('No hay datos para copiar');
        return;
    }

    let text = '';
    table.querySelectorAll('tr').forEach(tr => {
        const row = Array.from(tr.querySelectorAll('th, td'))
            .map(td => td.textContent.trim())
            .join('\t');
        text += row + '\n';
    });

    navigator.clipboard.writeText(text).then(() => {
        alert('Datos copiados al portapapeles');
    }).catch(err => {
        console.error('Error al copiar:', err);
        alert('Error al copiar datos');
    });
};

/**
 * Export GridJS table data to Excel.
 * @param {string} filename - Name of the Excel file (without extension)
 */
GridUtils.exportToExcel = function(filename = 'export') {
    const table = document.querySelector('.gridjs-table');
    if (!table) {
        alert('No hay datos para exportar');
        return;
    }

    const wb = XLSX.utils.table_to_book(table, { sheet: 'Datos' });
    const ws = wb.Sheets[wb.SheetNames[0]];

    const colWidths = [];
    const headers = table.querySelectorAll('thead th');
    headers.forEach((th, i) => {
        const maxWidth = Math.max(
            th.textContent.trim().length,
            ...Array.from(table.querySelectorAll(`tbody td:nth-child(${i + 1})`))
                .map(td => td.textContent.trim().length)
        );
        colWidths.push({ wch: maxWidth + 2 });
    });
    ws['!cols'] = colWidths;

    XLSX.writeFile(wb, filename + '.xlsx');
};

/**
 * Add export buttons toolbar above GridJS table.
 * @param {string} containerId - ID of the container where to add buttons
 * @param {string} gridContainerId - ID of the GridJS container
 * @param {string} filename - Default filename for Excel export
 */
GridUtils.addToolbar = function(containerId, gridContainerId, filename = 'export') {
    const container = document.getElementById(containerId);
    if (!container) return;

    const toolbar = document.createElement('div');
    toolbar.className = 'd-flex gap-2 mb-3';
    toolbar.innerHTML = `
        <button type="button" class="btn btn-outline-secondary btn-sm"
                onclick="window.GridUtils.copyToClipboard()">
            <span class="material-icons" style="font-size: 1rem;">content_copy</span> Copiar
        </button>
        <button type="button" class="btn btn-outline-success btn-sm"
                onclick="window.GridUtils.exportToExcel('${filename}')">
            <span class="material-icons" style="font-size: 1rem;">download</span> Excel
        </button>
    `;

    const gridContainer = document.getElementById(gridContainerId);
    if (gridContainer && gridContainer.parentNode) {
        gridContainer.parentNode.insertBefore(toolbar, gridContainer);
    }
};

/**
 * Standard error handler for GridJS server requests.
 */
GridUtils.handleServerError = function(res) {
    if (res.ok) return res.json();
    throw new Error('Error al cargar datos: ' + res.status);
};

window.GridUtils = GridUtils;