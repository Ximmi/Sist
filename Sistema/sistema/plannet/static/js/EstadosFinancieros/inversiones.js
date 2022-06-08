function calcular(params) {
    $('#id_total').val($('#id_socios').val() + $('#id_bancos').val() + $('#id_gobiernof').val() + $('#id_gobiernoe').val() + $('#id_otras').val() );
}
$('#id_socios').change(
    function(){
        calcular();
    }
);
$('#id_bancos').change(
    function(){
        calcular();
    }
);
$('#id_gobiernof').change(
    function(){
        calcular();
    }
);
$('#id_gobiernoe').change(
    function(){
        calcular();
    }
);
$('#id_otras').change(
    function(){
        calcular();
    }
);