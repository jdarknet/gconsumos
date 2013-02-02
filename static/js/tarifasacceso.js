/**
 * Created with PyCharm.
 * User: julian
 * Date: 19/01/13
 * Time: 12:24
 * To change this template use File | Settings | File Templates.
 */


;( function($) {

    function llenacombo()
    {
        var idperiodo  =  $("#id_cabperiodo").val();
        var nfila      =  $('#id_detallestarifas_set-INITIAL_FORMS').val();
        var totfila    =  $('#id_detallestarifas_set-TOTAL_FORMS').val();
        if ( !isNaN(idperiodo) && idperiodo.length!=0 && idperiodo !=undefined  )
        {

            for (var numerolineas=0 ; numerolineas <totfila ; numerolineas++)
            {

                var valor =$('#id_detallestarifas_set-'+numerolineas+'-detperiodo').val();
                if( isNaN(valor) || valor==undefined ||valor.length==0 )
                {
                    valor=0;

                }

                Dajaxice.web.llenaPeriodos(Dajax.process,{'valor':valor, 'numero': numerolineas,'id': idperiodo});
            }
        }

    }
    $(document).ready( function() {

        llenacombo();

        $('#id_cabperiodo').blur(function(event)
        {
            llenacombo();
        });
        $('tr.add-row >td >a').mouseover(function(e)
            {
                var idperiodo  =  $("#id_cabperiodo").val();
                var valor =0;
                var numerolineas = $('#id_detallestarifas_set-TOTAL_FORMS').val()+1;
                Dajaxice.web.llenaPeriodos(Dajax.process,{'valor':valor, 'numero': numerolineas,'id': idperiodo});

            }
        );

     });



})(django.jQuery);