function calcular(params) {
    $('#id_pago_anual').val($('#id_pago_mensual').val()*12);
    $('#id_prestaciones').val($('#id_pago_mensual').val()*3.6);
    $('#id_total_anual').val($('#id_pago_mensual').val()*3.6*$('#id_numero_personas').val());
}

$('#id_pago_mensual').on('change', function () {
    calcular();
})

$('#id_numero_personas').on('change', function () {
    calcular();
})