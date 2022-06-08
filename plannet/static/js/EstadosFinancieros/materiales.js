function calcular(params) {
    $('#id_costo_anual').val($('#id_costo').val()*$('#id_volumen').val());
}
$('#id_costo').change(
    function(){
        calcular();
    }
);
$('#id_volumen').change(
    function(){
        calcular();
    }
);
