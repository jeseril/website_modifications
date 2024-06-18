odoo.define('website_modifications.add_dolar_web',[], function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function() {
        getTRMValue();
    });

    function getTRMValue() {
        $.ajax({
            url: '/get_trm_value',
            type: 'GET',
            success: function(data) {
                        if (data !== "No se encontró ningún valor de TRM en la base de datos") {
                            const trmValue = parseFloat(data);
                            const formattedTRM = trmValue.toLocaleString();
                            $('#valor-y-cambio').html('<p>TRM</p><div class="contenedor_dolar"><span class="numero_dinero">$ ' + formattedTRM + '</span></div>');
                        } else {
                    console.error("Error retrieving TRM value:", data);
                }
            },
            error: function(error) {
                console.error("Error fetching TRM value:", error);
            }
        });
    }
});