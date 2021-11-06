jQuery(function () {
    var myChart = NaN;

    var chartTooltip = {
        backgroundColor: foregroundColor,
        titleFontColor: primaryColor,
        borderColor: separatorColor,
        borderWidth: 0.5,
        bodyFontColor: primaryColor,
        bodySpacing: 10,
        xPadding: 15,
        yPadding: 15,
        cornerRadius: 0.15,
        displayColors: false
      };

    var rootStyle = getComputedStyle(document.body);
    var themeColor1 = rootStyle.getPropertyValue("--theme-color-1").trim();
    var themeColor1_10 = rootStyle
      .getPropertyValue("--theme-color-1-10")
      .trim();

    var primaryColor = rootStyle.getPropertyValue("--primary-color").trim();
    var foregroundColor = rootStyle
      .getPropertyValue("--foreground-color")
      .trim();
    var separatorColor = rootStyle.getPropertyValue("--separator-color").trim();

    Chart.defaults.LineWithShadow = Chart.defaults.line;
      Chart.controllers.LineWithShadow = Chart.controllers.line.extend({
        draw: function (ease) {
          Chart.controllers.line.prototype.draw.call(this, ease);
          var ctx = this.chart.ctx;
          ctx.save();
          ctx.shadowColor = "rgba(0,0,0,0.15)";
          ctx.shadowBlur = 10;
          ctx.shadowOffsetX = 0;
          ctx.shadowOffsetY = 10;
          ctx.responsive = true;
          ctx.stroke();
          Chart.controllers.line.prototype.draw.apply(this, arguments);
          ctx.restore();
        }
      });

    function draw(station, vev) {
        var visitChart = document.getElementById("aquChart").getContext("2d");
        myChart = new Chart(visitChart, {
            type: "LineWithShadow",
            options: {
                plugins: {
                    datalabels: {
                        display: false
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    yAxes: [
                        {
                            gridLines: {
                                display: true,
                                lineWidth: 1,
                                color: "rgba(0,0,0,0.1)",
                                drawBorder: false
                            },
                            ticks: {
                                beginAtZero: true,
                                stepSize: 5,
                                min: 50,
                                max: 70,
                                padding: 0
                            }
                        }
                    ],
                    xAxes: [
                        {
                            gridLines: {
                                display: false
                            }
                        }
                    ]
                },
                legend: {
                    display: false
                },
                tooltips: chartTooltip
            },
            data: {
                labels: data['label'],
                datasets: [
                    {
                        label: "",
                        data: data[station][vev],
                        borderColor: themeColor1,
                        pointBackgroundColor: foregroundColor,
                        pointBorderColor: themeColor1,
                        pointHoverBackgroundColor: themeColor1,
                        pointHoverBorderColor: foregroundColor,
                        pointRadius: 4,
                        pointBorderWidth: 2,
                        pointHoverRadius: 5,
                        fill: true,
                        borderWidth: 2,
                        backgroundColor: themeColor1_10
                    }
                ]
            }
        });
    }

    draw(11, 'co');

    $('#id_station').change(function () {
        var vesh = $('#id_vevo').val();
        var s = $(this).val();
        draw(s,vesh);
    });

    $('#id_vevo').change(function () {
        var vesh = $(this).val();
        var s = $('#id_station').val();
        draw(s,vesh);
    });

});