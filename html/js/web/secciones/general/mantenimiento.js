(function() {

    CallBackTime = (function()
    {
        $('#modal').modal();
        shortly = new Date();
        shortly.setSeconds(shortly.getSeconds() + 40);

        $('#conteo').countdown({until: shortly, expiryUrl: "http://" + $('#id_configura-w_ip').val() ,
            description: 'Esperar para conectar a la  nueva direccion' ,format : 'MS' });

        $('#conteo').countdown('option', {until: shortly ,format: 'MS'});
    }
        )

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
        $('#envia_archivo').spin(false);

        $('#envia_archivo').click( function(e){
            $('#envia_archivo').spin();
        });

        $("#id_fecha").datepicker({dateFormat:"d-m-yy"});
        new ConfirmAction($("#fix-eliminar"));



    });

}).call(this);

