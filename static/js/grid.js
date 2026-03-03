/**
 * Grid.js initialization utilities for Boa POS.
 * Provides helper functions to create dynamic data tables with Grid.js.
 */

const GridJS = window.GridJS || {};

/**
 * Initialize a Grid.js table with given configuration.
 * @param {string} tableId - DOM ID for the table element.
 * @param {string} apiUrl - URL endpoint for fetching data.
 * @param {Array} columns - Column definitions.
 * @param {Object} options - Additional Grid.js options.
 */
GridJS.init = function(tableId, apiUrl, columns, options = {}) {
    const tableElement = document.getElementById(tableId);
    if (!tableElement) {
        console.error(`GridJS: Table element #${tableId} not found`);
        return null;
    }

    const defaultOptions = {
        columns: columns,
        data: {
            url: apiUrl
        },
        search: true,
        sort: true,
        pagination: {
            limit: 10,
            summary: true
        },
        resizable: true,
        language: {
            search: {
                placeholder: 'Buscar...'
            },
            pagination: {
                previous: 'Anterior',
                next: 'Siguiente',
                showing: 'Mostrando',
                of: 'de',
                to: 'a',
                results: 'resultados'
            }
        }
    };

    const mergedOptions = { ...defaultOptions, ...options };

    if (typeof window.Grid !== 'undefined') {
        return new window.Grid(mergedOptions).render(tableElement);
    }

    console.error('Grid.js library not loaded');
    return null;
};

/**
 * Initialize a Grid.js table with local data.
 * @param {string} tableId - DOM ID for the table element.
 * @param {Array} data - Local data array.
 * @param {Array} columns - Column definitions.
 * @param {Object} options - Additional Grid.js options.
 */
GridJS.initLocal = function(tableId, data, columns, options = {}) {
    const tableElement = document.getElementById(tableId);
    if (!tableElement) {
        console.error(`GridJS: Table element #${tableId} not found`);
        return null;
    }

    const defaultOptions = {
        columns: columns,
        data: data,
        search: true,
        sort: true,
        pagination: {
            limit: 10,
            summary: true
        },
        language: {
            search: {
                placeholder: 'Buscar...'
            },
            pagination: {
                previous: 'Anterior',
                next: 'Siguiente',
                showing: 'Mostrando',
                of: 'de',
                to: 'a',
                results: 'resultados'
            }
        }
    };

    const mergedOptions = { ...defaultOptions, ...options };

    if (typeof window.Grid !== 'undefined') {
        return new window.Grid(mergedOptions).render(tableElement);
    }

    console.error('Grid.js library not loaded');
    return null;
};

/**
 * Factory function to create column definitions from model fields.
 * @param {Array} fields - Array of field config objects {name, id, width, hidden}.
 * @returns {Array} Grid.js column definitions.
 */
GridJS.createColumns = function(fields) {
    return fields.map(function(field) {
        const col = {
            name: field.name,
            id: field.id || field.name.toLowerCase()
        };
        if (field.width) col.width = field.width;
        if (field.hidden) col.hidden = field.hidden;
        if (field.sort !== undefined) col.sort = field.sort;
        if (field.formatter) col.formatter = field.formatter;
        return col;
    });
};

/**
 * Add column filters to a Grid.js table.
 * @param {string} tableId - DOM ID of the table container.
 * @param {string} filterPlaceholder - Placeholder text for filter inputs.
 */
GridJS.addColumnFilters = function(tableId, filterPlaceholder = 'Filtrar...') {
    const container = document.getElementById(tableId);
    if (!container) {
        console.warn(`GridJS: Table container #${tableId} not found`);
        return;
    }
    
    setTimeout(function() {
        const table = container.querySelector('.gridjs-table');
        if (!table) return;
        
        const thead = table.querySelector('thead');
        if (!thead) return;
        
        const headerRow = thead.querySelector('tr');
        if (!headerRow) return;
        
        // Check if filter row already exists
        if (thead.querySelector('.gridjs-filter-row')) return;
        
        const filterRow = document.createElement('tr');
        filterRow.className = 'gridjs-filter-row';
        
        const cols = headerRow.querySelectorAll('th');
        const colCount = cols.length;
        const filterValues = new Array(colCount).fill('');
        
        function applyAllFilters() {
            const tbody = table.querySelector('tbody');
            if (!tbody) return;
            
            const rows = tbody.querySelectorAll('tr');
            rows.forEach(function(row) {
                const cells = row.querySelectorAll('td');
                let showRow = true;
                
                for (let i = 0; i < colCount; i++) {
                    const filterValue = filterValues[i].toLowerCase().trim();
                    if (filterValue === '') continue;
                    
                    const cellText = cells[i] ? cells[i].textContent.toLowerCase() : '';
                    if (cellText.indexOf(filterValue) === -1) {
                        showRow = false;
                        break;
                    }
                }
                
                row.style.display = showRow ? '' : 'none';
            });
        }
        
        cols.forEach(function(th, colIndex) {
            const newTh = document.createElement('th');
            newTh.className = 'gridjs-th';
            
            const inputWrapper = document.createElement('div');
            inputWrapper.className = 'gridjs-filter-wrapper';
            
            const input = document.createElement('input');
            input.type = 'text';
            input.placeholder = filterPlaceholder;
            input.className = 'gridjs-filter-input';
            input.setAttribute('data-col-index', colIndex);
            
            input.addEventListener('keyup', function() {
                filterValues[colIndex] = input.value;
                applyAllFilters();
            });
            
            inputWrapper.appendChild(input);
            newTh.appendChild(inputWrapper);
            filterRow.appendChild(newTh);
        });
        
        thead.appendChild(filterRow);
    }, 300);
};

window.GridJS = GridJS;
