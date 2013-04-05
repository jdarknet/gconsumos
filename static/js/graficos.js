/**
 * Created with PyCharm.
 * User: julian
 * Date: 23/11/12
 * Time: 21:05
 * Gestion de graficos del inicio del panel de control.
 */

(function($) {
    function ponGraficos(nomprocedure,nomgrafico)
    {
        var valores=[];
        $.getJSON($SCRIPT_ROOT + '/'+nomprocedure,
            function(data){
                var arreglo =[];
                var intvalores =[];
                var xy =[];
                var ax =[];
                var ay =[];
                var x, y,a;
                valores = data.result;
                for( i=0 ; i < valores.length ; i++)
                {
                    a=valores[i].toString()
                    xy =a.split(",").map(function(x){return parseInt(x)})
                    ax.push(xy[0]);
                    ay.push(xy[1]);
                    intvalores.push(xy);
                }
                ;
                var maximoy = Math.max.apply(Math,ay);
                var maximox = Math.max.apply(Math,ax)
                var options = {
                    yaxis: { min: 0, max: maximoy+100 },
                    xaxis: { min: 0, max: maximox },
                    colors: ["#EDC240", "#222", "#666", "#BBB"],
                    series: {
                        lines: {
                            lineWidth: 2,
                            fill: true,
                            fillColor: { colors: [ { opacity: 0.3 }, { opacity: 0.03 } ] },
                            steps: false
                        }

                    }
                };




                fecthed ={label:"Watts" , data: intvalores}
                arreglo.push(fecthed)
                var plot = $.plot($("#"+nomgrafico),arreglo  , options)


            });


    }




})(jQuery);