function calcular(params) {
    $('#id_ingresos').val($('#id_unidades').val()*$('#id_precio_unitario').val());
}
$('#id_unidades').change(
    function(){
        calcular();
    }
);
$('#id_precio_unitario').change(
    function(){
        calcular();
    }
);
