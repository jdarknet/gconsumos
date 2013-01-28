/**
 * Created with PyCharm.
 * User: julian
 * Date: 19/01/13
 * Time: 12:24
 * To change this template use File | Settings | File Templates.
 */
;( function($) {

    $(document).ready( function() {



        $('#id_cabperiodo').blur(function(event)
        {
//            var nfilas     =  $('table > tbody').length-1
            var idperiodo  =  $(this).val();

            var nfila      =  $('#id_detallestarifas_set-INITIAL_FORMS').val();
            var totfila    =  $('#id_detallestarifas_set-TOTAL_FORMS').val();
            if ( !isNaN(idperiodo) && idperiodo.length!=0 && idperiodo !=undefined  )
            {

                for (var numerolineas=nfila ; numerolineas <totfila ; numerolineas++)
                {
                    alert(numerolineas);
                    Dajaxice.web.llenaPeriodos(Dajax.process,{'numero': numerolineas,'id': idperiodo});
                }
            }

        });



    });



})(django.jQuery);