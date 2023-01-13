function calcular(params) {
    socios = Number($('#id_socios').val())
    bancos = Number($('#id_bancos').val())
    gobof = Number($('#id_gobiernof').val())
    gobe= Number($('#id_gobiernoe').val())
    otras = Number($('#id_otras').val())
    total = Number(socios + bancos + gobof + gobe + otras)
    Number($('#id_total').val(total))
    //$('#id_total').val(Number($('#id_socios').val()*1)+ Number($('#id_bancos').val()*12) + Number($('#id_gobiernof').val()*12) + Number($('#id_gobiernoe').val()*12) + Number($('#id_otras').val()*12) );
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