(function() {
    ConfirmAction = (function() {

        function ConfirmAction(container) {
            var _this = this;
            this.container = container;
            this.link = this.container.find("a[rel='action']");
            this.confirm = this.container.find("[rel='confirm-action']");
            this.link.click(function() {
                return _this.confirm.fadeIn();
            });
            this.cancelLink = this.container.find("a[rel='confirm-cancel']");
            this.confirmLink = this.container.find("a[rel='confirm-eliminar']");
            this.confirmLink.hide();

            this.confirmLink.click(function() {
               $("#fix-eliminar").spin();
                Dajaxice.web.limpiarTablasLecturas(Dajax.process);
                return _this.container.slideUp();
            });
            this.confirmCheck = this.container.find("[rel='confirm-check']");
            this.cancelLink.click(function() {
                _this.confirm.fadeOut();
                _this.confirmCheck.removeAttr("checked");

                return _this.confirmLink.hide();
            });
            this.confirmCheck.change(function() {
                if (_this.confirmCheck.attr("checked") === "checked") {
                    return _this.confirmLink.fadeIn();
                } else {
                    return _this.confirmLink.fadeOut();
                }
            });
        }

        return ConfirmAction;

    })();

    $(function() {

//        $.ajax({
//            url:'/general/configuracion/',
//            type: 'POST',
//            success: function(data) {
//                if( data.form_saved ){
//
//                    alert("Entra");
//
//                    $('#form input').removeClass('error'); // Form submit ok -> remove error class of all fields
//
//                    var chart_data = data.chart_data;
//                    // Update the chart here
//
//                }else{
//                    var form_errors = data.form_errors;
//
//                    // Display form validation errors
//                    for(var fieldname in form_errors) {
//
//                        var errors = form_errors[fieldname];       // Array of error strings for fieldname
//
//                        $('#form input[name="'+fieldname+']').addClass('error')
//                        alert(errors)
//
//                    }
//                }
//            }
//        });

        $("#ips").toggle(!$('#id_configura-w_dhcp').attr('checked'));
        $('#id_configura-w_dhcp').click(function() { $("#ips").toggle(!this.checked);} );


//        $('#limpiar').click(function(){
//             $('#modal').modal()
//               });

        var tipo = $('#id_configura-protvolcado').val()

        if(tipo=="email")
        {
            $('#email').toggle(true);

        }else
        {
            $('#email').toggle(false);
        }
        if(tipo in {"ftp":"","ssh":""} )
        {
            $('#ftp').toggle(true);
        }
        else
        {
            $('#ftp').toggle(false);
        }


        $('#id_configura-protvolcado').change(function(){
            var etiq = $(this).val()

            if(etiq=="email")
            {
                $('#email').toggle(true);
            }
            else
            {
                $('#email').toggle(false);
            }
            if(etiq in  {"ftp":"","ssh":""})
            {
                $('#ftp').toggle(true);
            }
            else
            {
                $('#ftp').toggle(false);

            }

        });

        $('#busca_wifi').click( function(e){
            $('#essid').spin();
            Dajaxice.web.updatewifis(Dajax.process);
        }) ;

        $('#conectar_wifi').click( function(e){
            $('#essid').spin();
            if($('#id_configura-w_dhcp').attr('checked'))
            {
                var dhcp = "S";
            }
            else
            {
                var dhcp = "N";
            }
            var ip     = $('#id_configura-w_ip').val();
            var mask   = $('#id_configura-w_mask').val();
            var gw     = $('#id_configura-w_gw').val();
            var essid  = $('#id_configura-essid').val();
            var passwd = $('#id_configura-password').val();

            Dajaxice.web.conectarwifi(Dajax.process,{'ip':ip,'mask':mask,'gw':gw,'essid':essid,'passwd':passwd,'dhcp':dhcp});

        }) ;


        $("#id_configura-fecha").datepicker({dateFormat:"d-m-yy"});
        new ConfirmAction($("#fix-eliminar"));


    });

}).call(this);
