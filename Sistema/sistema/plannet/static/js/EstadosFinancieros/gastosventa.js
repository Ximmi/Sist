function calcular(params) {
    $('#id_gasto_anual').val($('#id_gasto_unidad').val()*$('#id_cantidad').val());
}
$('#id_gasto_unidad').change(
    function(){
        calcular();
    }
);
$('#id_cantidad').change(
    function(){
        calcular();
    }
);