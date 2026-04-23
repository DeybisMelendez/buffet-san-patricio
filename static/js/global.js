/**
 * Buffet San Patricio - Global JavaScript
 * Reemplaza AlpineJS con JavaScript vanilla simple y legible.
 */

(function() {
    'use strict';

    // ============================================
    // UTILIDADES PARA ALERTAS/MENSAJES
    // ============================================

    window.AppUtils = {
        hideAlerts: function() {
            var alerts = document.querySelectorAll('.alert');
            alerts.forEach(function(alert) {
                alert.style.display = 'none';
            });
        },

        initAlerts: function() {
            var closeBtns = document.querySelectorAll('.alert button[data-bs-dismiss]');
            closeBtns.forEach(function(btn) {
                btn.addEventListener('click', function() {
                    var alert = btn.closest('.alert');
                    if (alert) {
                        alert.style.display = 'none';
                    }
                });
            });
        }
    };

    // ============================================
    // DATETIME UPDATER (navbar)
    // ============================================

    function DateTimeUpdater() {
        this.timeEl = document.querySelector('[data-datetime-time]');
        this.dateEl = document.querySelector('[data-datetime-date]');
        if (!this.timeEl && !this.dateEl) return;

        this.update();
        setInterval(function() {
            this.update();
        }.bind(this), 1000);
    }

    DateTimeUpdater.prototype.update = function() {
        var now = new Date();
        var timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit' };
        var dateOptions = { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' };

        if (this.timeEl) {
            this.timeEl.textContent = now.toLocaleTimeString('es-NI', timeOptions);
        }
        if (this.dateEl) {
            this.dateEl.textContent = now.toLocaleDateString('es-NI', dateOptions);
        }
    };

    // ============================================
    // INVOICE FORM (facturas)
    // ============================================

    window.initInvoiceForm = function(total) {
        var form = document.querySelector('[data-invoice-form]');
        if (!form) return;

        var paymentType = form.querySelector('[name="payment_type"]');
        var amountReceived = form.querySelector('[name="amount_received"]');
        var changeEl = form.querySelector('[data-change]');
        var submitCash = form.querySelector('[data-submit-cash]');
        var submitCredit = form.querySelector('[data-submit-credit]');

        function updateChange() {
            if (!amountReceived || !changeEl) return;
            var received = parseFloat(amountReceived.value) || 0;
            var change = received - total;
            changeEl.textContent = change.toFixed(2);
        }

        function updateVisibility() {
            var type = paymentType ? paymentType.value : 'PENDIENTE';
            var received = parseFloat(amountReceived ? amountReceived.value : 0) || 0;

            // Toggle efectivo fields
            var efectivoFields = form.querySelectorAll('[data-show-if-efectivo]');
            efectivoFields.forEach(function(el) {
                el.style.display = type === 'EFECTIVO' ? '' : 'none';
            });

            // Toggle buttons
            if (submitCredit) submitCredit.style.display = type === 'PENDIENTE' ? '' : 'none';
            if (submitCash) {
                submitCash.style.display = type !== 'PENDIENTE' ? '' : 'none';
                if (type === 'EFECTIVO' && received < total) {
                    submitCash.disabled = true;
                } else {
                    submitCash.disabled = false;
                }
            }

            updateChange();
        }

        if (paymentType) {
            paymentType.addEventListener('change', updateVisibility);
        }
        if (amountReceived) {
            amountReceived.addEventListener('input', updateVisibility);
        }

        updateVisibility();
    };

    // ============================================
    // INVENTORY ADJUSTMENT (ajuste de inventario)
    // ============================================

    window.initInventoryAdjust = function() {
        var rows = document.querySelectorAll('[data-inventory-row]');
        rows.forEach(function(row) {
            var foundInput = row.querySelector('[data-found]');
            var diffEl = row.querySelector('[data-diff]');
            if (!foundInput || !diffEl) return;

            foundInput.addEventListener('input', function() {
                var actual = parseFloat(row.dataset.actual) || 0;
                var found = parseFloat(foundInput.value) || 0;
                var diff = found - actual;
                diffEl.textContent = diff.toFixed(2);
                diffEl.className = 'text-end';
                if (diff > 0) diffEl.classList.add('text-success');
                else if (diff < 0) diffEl.classList.add('text-danger');
            });
        });
    };

    // ============================================
    // FOOD CONVERTER (conversor de alimentos)
    // ============================================

    window.initFoodConverter = function(recipes) {
        var modeBtns = document.querySelectorAll('[data-mode-btn]');
        var recipeSelect = document.querySelector('[data-recipe-select]');
        var factorInput = document.querySelector('[data-factor-input]');
        var previewEl = document.querySelector('[data-recipe-preview]');

        function showMode(mode) {
            var recipePanel = document.querySelector('[data-mode-recipe]');
            var manualPanel = document.querySelector('[data-mode-manual]');
            if (recipePanel) recipePanel.style.display = mode === 'recipe' ? '' : 'none';
            if (manualPanel) manualPanel.style.display = mode === 'manual' ? '' : 'none';

            modeBtns.forEach(function(btn) {
                var btnMode = btn.dataset.modeBtn;
                btn.classList.toggle('active', btnMode === mode);
            });
        }

        function updatePreview() {
            if (!recipeSelect || !previewEl || !factorInput) return;
            var recipeId = recipeSelect.value;
            var factor = parseFloat(factorInput.value) || 1;

            if (!recipeId || !recipes[recipeId]) {
                previewEl.innerHTML = '';
                return;
            }

            var recipe = recipes[recipeId];
            var html = '<div class="row"><div class="col-md-6">' +
                '<h6 class="text-danger">Entradas (Consumo)</h6><table class="table table-sm">';

            recipe.items.filter(function(i) { return i.is_input; }).forEach(function(item) {
                var qty = (item.quantity * factor).toFixed(2) + ' ' + item.unit;
                html += '<tr><td>' + item.name + '</td><td class="text-end">' + qty + '</td></tr>';
            });

            html += '</table></div><div class="col-md-6">' +
                '<h6 class="text-success">Salidas (Procesado)</h6><table class="table table-sm">';

            recipe.items.filter(function(i) { return !i.is_input; }).forEach(function(item) {
                var qty = (item.quantity * factor).toFixed(2) + ' ' + item.unit;
                html += '<tr><td>' + item.name + '</td><td class="text-end">' + qty + '</td></tr>';
            });

            html += '</table></div></div>';
            previewEl.innerHTML = html;
        }

        modeBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                showMode(btn.dataset.modeBtn);
            });
        });

        if (recipeSelect) recipeSelect.addEventListener('change', updatePreview);
        if (factorInput) factorInput.addEventListener('input', updatePreview);

        showMode('recipe');
    };

    // ============================================
    // FOOD RECIPE FORM (formulario de recetas)
    // ============================================

    window.initFoodRecipeForm = function(initialInputCount, initialOutputCount) {
        var inputContainer = document.querySelector('[data-input-rows]');
        var outputContainer = document.querySelector('[data-output-rows]');
        var addInputBtn = document.querySelector('[data-add-input]');
        var addOutputBtn = document.querySelector('[data-add-output]');

        function createRow(uid, ingredient, quantity, type) {
            var row = document.createElement('div');
            row.className = 'row g-2 mb-2 align-items-end';
            row.dataset.rowUid = uid;

            var ingredientOptions = document.querySelector('[data-ingredient-options]');
            var optionsHtml = ingredientOptions ? ingredientOptions.innerHTML : '';

            row.innerHTML =
                '<div class="col-7">' +
                    '<label class="form-label small">Ingrediente</label>' +
                    '<select name="ing_' + uid + '" class="form-select form-select-sm">' + optionsHtml + '</select>' +
                '</div>' +
                '<div class="col-3">' +
                    '<label class="form-label small">Cantidad</label>' +
                    '<input type="number" name="qty_' + uid + '" value="' + quantity + '" step="0.01" min="0" class="form-control form-control-sm">' +
                '</div>' +
                '<div class="col-2">' +
                    '<button type="button" class="btn btn-outline-danger btn-sm" onclick="removeRow(' + uid + ', \'' + type + '\')">' +
                        '<span class="material-icons">close</span>' +
                    '</button>' +
                '</div>' +
                '<input type="hidden" name="type_' + uid + '" value="' + type + '">';

            // Set selected ingredient
            var select = row.querySelector('select');
            if (ingredient) {
                select.value = ingredient;
            }

            return row;
        }

        window.addInputRow = function() {
            if (!inputContainer) return;
            var uid = Date.now();
            inputContainer.appendChild(createRow(uid, '', 0, 'input'));
            updateTotalForms();
        };

        window.addOutputRow = function() {
            if (!outputContainer) return;
            var uid = Date.now() + 1000;
            outputContainer.appendChild(createRow(uid, '', 0, 'output'));
            updateTotalForms();
        };

        window.removeRow = function(uid, type) {
            var container = type === 'input' ? inputContainer : outputContainer;
            if (!container) return;
            var row = container.querySelector('[data-row-uid="' + uid + '"]');
            if (row) {
                // Mark for deletion if it's an existing row
                var deleteInput = row.querySelector('input[name$="-DELETE"]');
                if (deleteInput) {
                    deleteInput.checked = true;
                }
                row.style.display = 'none';
            }
            updateTotalForms();
        };

        function updateTotalForms() {
            var totalForms = document.getElementById('id_form-TOTAL_FORMS');
            if (totalForms) {
                var rows = document.querySelectorAll('[data-input-rows] .row[data-row-uid], [data-output-rows] .row[data-row-uid]');
                totalForms.value = rows.length;
            }
        }

        if (addInputBtn) addInputBtn.addEventListener('click', window.addInputRow);
        if (addOutputBtn) addOutputBtn.addEventListener('click', window.addOutputRow);

        updateTotalForms();
    };

    // ============================================
    // PRODUCT RECIPES (recetas de producto)
    // ============================================

    window.initProductRecipes = function(initialCount) {
        var container = document.querySelector('[data-formset-container]');
        var addBtn = document.querySelector('[data-add-form]');
        var template = document.getElementById('empty-form-template');

        if (!container || !template) return;

        window.addRecipeForm = function() {
            var newRow = template.content.cloneNode(true);
            var newIndex = Date.now();

            newRow.querySelectorAll('input, select, label').forEach(function(el) {
                if (el.name) el.name = el.name.replace(/__prefix__/g, newIndex);
                if (el.id) el.id = el.id.replace(/__prefix__/g, newIndex);
                if (el.htmlFor) el.htmlFor = el.htmlFor.replace(/__prefix__/g, newIndex);
            });

            var tr = newRow.querySelector('tr');
            tr.setAttribute('data-form-index', newIndex);

            var deleteBtn = tr.querySelector('.delete-row');
            if (deleteBtn) {
                deleteBtn.addEventListener('click', function() {
                    var row = container.querySelector('[data-form-index="' + newIndex + '"]');
                    if (row) {
                        var del = row.querySelector('input[name$="-DELETE"]');
                        if (del) del.checked = true;
                        row.style.display = 'none';
                    }
                });
            }

            container.appendChild(newRow);
            updateFormCount();
        };

        window.removeRecipeForm = function(index, hasPk) {
            var row = container.querySelector('[data-form-index="' + index + '"]');
            if (row) {
                var del = row.querySelector('input[name$="-DELETE"]');
                if (del) del.checked = true;
                row.style.display = 'none';
            }
            updateFormCount();
        };

        function updateFormCount() {
            var totalForms = document.getElementById('id_form-TOTAL_FORMS');
            if (totalForms) {
                var rows = container.querySelectorAll('.formset-row:not([style*="display: none"])');
                totalForms.value = rows.length;
            }
        }

        if (addBtn) addBtn.addEventListener('click', window.addRecipeForm);

        // Add click handlers to existing delete buttons
        container.querySelectorAll('.delete-row').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var row = btn.closest('tr');
                if (row) {
                    var del = row.querySelector('input[name$="-DELETE"]');
                    if (del) del.checked = true;
                    row.style.display = 'none';
                    updateFormCount();
                }
            });
        });

        updateFormCount();
    };

    // ============================================
    // PRINT FUNCTIONS
    // ============================================

    window.printOrder = function(orderId, iframeId) {
        var iframe = document.getElementById(iframeId);
        if (!iframe) return;

        fetch('/pos/order/' + orderId + '/print/')
            .then(function(response) { return response.text(); })
            .then(function(html) {
                iframe.srcdoc = html;
            })
            .catch(function(err) {
                console.error('Error printing order:', err);
            });
    };

    window.printInventoryReport = function(iframeId) {
        var iframe = document.getElementById(iframeId);
        if (!iframe) return;

        fetch('/reports/inventory/print/')
            .then(function(response) { return response.text(); })
            .then(function(html) {
                iframe.srcdoc = html;
            })
            .catch(function(err) {
                console.error('Error printing report:', err);
            });
    };

    // ============================================
    // MODAL HANDLER (edit_order)
    // ============================================

    window.initModalConfirm = function() {
        var form = document.querySelector('[data-edit-order-form]');
        var modal = document.getElementById('confirmModal');
        var modalInstance = null;

        if (typeof bootstrap !== 'undefined' && modal) {
            modalInstance = new bootstrap.Modal(modal);
        }

        var saveBtn = document.querySelector('[data-save-btn]');
        if (saveBtn) {
            saveBtn.addEventListener('click', function(e) {
                e.preventDefault();
                if (modalInstance) {
                    modalInstance.show();
                } else {
                    form.submit();
                }
            });
        }

        var confirmBtn = document.querySelector('[data-confirm-btn]');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', function() {
                form.submit();
            });
        }
    };

    // ============================================
    // INITIALIZATION
    // ============================================

    document.addEventListener('DOMContentLoaded', function() {
        // Init alerts
        AppUtils.initAlerts();

        // Init datetime updater
        new DateTimeUpdater();

        // Init invoice forms
        var invoiceForm = document.querySelector('[data-invoice-form]');
        if (invoiceForm) {
            var total = parseFloat(invoiceForm.dataset.total) || 0;
            initInvoiceForm(total);
        }

        // Init update payment form
        var updatePaymentForm = document.querySelector('[data-update-payment-form]');
        if (updatePaymentForm) {
            var total = parseFloat(updatePaymentForm.dataset.total) || 0;
            initInvoiceForm(total);
        }

        // Init inventory adjust
        initInventoryAdjust();

        // Init product recipes
        var productRecipesForm = document.querySelector('[data-product-recipes-form]');
        if (productRecipesForm) {
            var count = parseInt(productRecipesForm.dataset.formCount) || 0;
            initProductRecipes(count);
        }

        // Init modal confirm
        initModalConfirm();
    });

})();