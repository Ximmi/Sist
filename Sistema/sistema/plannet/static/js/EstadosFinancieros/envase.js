function calcular(params) {
    $('#id_costo_anual').val($('#id_costo').val()*$('#id_necesidad').val());
}
$('#id_costo').change(
    function(){
        calcular();
    }
);
$('#id_necesidad').change(
    function(){
        calcular();
    }
);
