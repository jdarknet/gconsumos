(function() {

    $(function() {

        $('#sensibilidad').hide()

        $('#id_mensajes tbody tr').formset({
            prefix: 'mensajes'
        });


        new Notifications({
            container: $("body"),
            bootstrapPositionClass: "span6 offset3"
        });


        var tipo = $('#id_cabalarma-tipo').val()
        if(tipo==1)
        {
            $('#id_cabalarma-consigna').attr("disabled","disabled");
            $('#horarios').hide()
            $('#sensibilidad').show()

        }

        $('#id_cabalarma-tipo').change(function(){
            var etiq = $(this).val()

            if(etiq=="1")
            {

                $('#id_cabalarma-consigna').attr("disabled","disabled");
                $('#horarios').hide()
                $('#sensibilidad').show()
            }
            else
            {
                $('#id_cabalarma-consigna').removeAttr('disabled');
                $('#horarios').show()
                $('sensibilidad').hide()
            }


        });

    });

}).call(this);

