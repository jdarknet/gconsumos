function ponGraficoDia(data)
{

    var valores=[];
    var arreglo =[];
    var intvalores =[];
    var xy =[];
    var ax =[];
    var ay =[];
    var x, y,a;
    valores = data;
    var i;
    for( i=0 ; i < valores.length ; i++)
    {
        a=valores[i].toString();
        xy =a.split(",").map(function(x){return parseInt(x)});
        ax.push(xy[0]);
        ay.push(xy[1]);
        intvalores.push(xy);
    }
    ;

    var maximoy = Math.max.apply(Math,ay);
    var maximox = Math.max.apply(Math,ax);
    var options = {
        yaxis: { min: 0, max: maximoy+100 },
        xaxis: {  mode: "time", timeformat:"%H:%M" },
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

    var fecthed ={label:"Watts" , data: intvalores};
    arreglo.push(fecthed);
    var plot = $.plot($("#chart1"),arreglo  , options);


};

function ponGraficoMesActual(data, etiqueta)
{

    var valores=[];
    var arreglo =[];
    var intvalores =[];
    var xy =[];
    var ax =[];
    var ay =[];
    var x, y,a;
    valores = data;
    var i;

    if ( etiqueta == undefined )
    {
        etiqueta="#chart2";
    }
    for( i=0 ; i < valores.length ; i++)
    {
        a=valores[i].toString();
        xy =a.split(",").map(function(x){return parseInt(x)})
        ax.push(xy[0]);
        ay.push(xy[1]);
        intvalores.push(xy);
    }
    ;

    var maximoy = Math.max.apply(Math,ay);
    var maximox = Math.max.apply(Math,ax);
    var options = {
        yaxis: { min: 0, max: maximoy+100 },
        xaxis: { mode:"time" },
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

    var fecthed ={label:"Watts" , data: intvalores};
    arreglo.push(fecthed);
    var plot = $.plot($(etiqueta),arreglo  , options);


};

function ponGraficoSemana(data)
{

    var valores=[];
    var arreglo =[];
    var intvalores =[];
    var xy =[];
    var ax =[];
    var ay =[];
    var x, y,a;
    valores = data;
    var i;

    for( i=0 ; i < valores.length ; i++)
    {
        a=valores[i].toString();
        xy =a.split(",").map(function(x){return parseInt(x)});
        ax.push(xy[0]);
        ay.push(xy[1]);
        intvalores.push(xy);
    }


    var maximoy = Math.max.apply(Math,ay);
    var maximox = Math.max.apply(Math,ax);
    var options = {
        yaxis: { min: 0, max: maximoy+100 },
        xaxis: { mode:'time', dayNames: ["dom", "lun", "mar", "mier", "jue", "vier", "sab"]
        },
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


    var fecthed ={label:"Watts" , data: intvalores};
    arreglo.push(fecthed);
    var plot = $.plot($("#chart1"), arreglo  , options);


};

function ponGraficoAno(data)
{

    var valores=[];
    var arreglo =[];
    var intvalores =[];
    var xy =[];
    var ax =[];
    var ay =[];
    var x, y,a;
    valores = data;
    var i;

    for( i=0 ; i < valores.length ; i++)
    {
        a=valores[i].toString();
        xy =a.split(",").map(function(x){return parseInt(x)});
        ax.push(xy[0]);
        ay.push(xy[1]);
        intvalores.push(xy);
    }


    var maximoy = Math.max.apply(Math,ay);
    var maximox = Math.max.apply(Math,ax);
    var options = {
        yaxis: { min: 0, max: maximoy+100 },
        xaxis: { mode:'time', timeformat:"%m"
        },
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


    var fecthed ={label:"Watts" , data: intvalores};
    arreglo.push(fecthed);
    var plot = $.plot($("#chart1"), arreglo  , options);


};

