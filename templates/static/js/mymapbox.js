$(document).ready(function () {
    let select = 0;
    let selectId = 0;
    let data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
    data['id'] = 11;
    data['name'] = $('#timeline_id_' + selectId).text();
    console.log(data);
    $.ajax({
        url: 'get_pred',
        type: 'POST',
        data: data,
        success: function (data) {
            $('#co').text(data.co.toFixed(2));
            $('#no').text(data.no.toFixed(2));
            $('#no2').text(data.no2.toFixed(2));
            $('#pm10').text(data.mp10.toFixed(2));
            $('#pm25').text(data.mp25.toFixed(2));
        }
    });

    function trans() {
        var wd = $(document).width();
        select = Math.round(wd / 2) - $('#timeline_id_0').width();
    }

    trans();
    window.onresize = function () {
        trans();
    };


    $('#timeline_id_0').css({'font-size': '14px', 'font-weight': '600'})
    $('.animate').css({"transform": `translate3d(${select}px, 0px, 0px)`});


    $('.timeline-item__time').on('click', function (e) {
        let clickId = parseInt($(this).attr('id').split('_')[2]);
        $('#timeline_id_' + selectId).css({'font-size': '13px', 'font-weight': '400'});
        $('#timeline_id_' + clickId).css({'font-size': '14px', 'font-weight': '600'});
        let width = $(this).width();
        var new_select = (selectId - clickId) * width;
        selectId = clickId;
        $('.animate').animate({
            'transform': new_select
        }, {
            step: function (now, fx) {
                $('.animate').css({"transform": `translate3d(${select + now}px, 0px, 0px)`});
            },
            complete: function () {
                select += new_select;
            },
            duration: 500,
            easing: 'linear',
            queue: false,
        }, 'linear');

        data['name'] = $('#timeline_id_' + selectId).text();
        $.ajax({
            url: 'get_pred',
            type: 'POST',
            data: data,
            success: function (data) {
                $('#co').text(data.co.toFixed(2));
                $('#no').text(data.no.toFixed(2));
                $('#no2').text(data.no2.toFixed(2));
                $('#pm10').text(data.mp10.toFixed(2));
                $('#pm25').text(data.mp25.toFixed(2));
            }
        });


    });
    $('.timeline__arrow_direction_right').click(function () {
        if (selectId < 71) {
            let clickId = selectId + 1;
            $('#timeline_id_' + selectId).css({'font-size': '13px', 'font-weight': '400'});
            $('#timeline_id_' + clickId).css({'font-size': '14px', 'font-weight': '600'});
            let width = $('#timeline_id_' + selectId).width();
            var new_select = (selectId - clickId) * width;
            selectId = clickId;
            $('.animate').animate({
                'transform': new_select
            }, {
                step: function (now, fx) {
                    console.log(now);
                    $('.animate').css({"transform": `translate3d(${select + now}px, 0px, 0px)`});
                },
                complete: function () {
                    select += new_select;
                },
                duration: 500,
                easing: 'linear',
                queue: false,
            }, 'linear');
            data['name'] = $('#timeline_id_' + selectId).text();
            $.ajax({
                url: 'get_pred',
                type: 'POST',
                data: data,
                success: function (data) {
                    $('#co').text(data.co.toFixed(2));
                    $('#no').text(data.no.toFixed(2));
                    $('#no2').text(data.no2.toFixed(2));
                    $('#pm10').text(data.mp10.toFixed(2));
                    $('#pm25').text(data.mp25.toFixed(2));
                }
            });
        }

    });

    $('.timeline__arrow_direction_left').click(function () {
        if (selectId > 0) {
            let clickId = selectId - 1;
            $('#timeline_id_' + selectId).css({'font-size': '13px', 'font-weight': '400'});
            $('#timeline_id_' + clickId).css({'font-size': '14px', 'font-weight': '600'});
            let width = $('#timeline_id_' + selectId).width();
            var new_select = (selectId - clickId) * width;
            selectId = clickId;
            $('.animate').animate({
                'transform': new_select
            }, {
                step: function (now, fx) {
                    console.log(now);
                    $('.animate').css({"transform": `translate3d(${select + now}px, 0px, 0px)`});
                },
                complete: function () {
                    select += new_select;
                },
                duration: 500,
                easing: 'linear',
                queue: false,
            }, 'linear');
            data['name'] = $('#timeline_id_' + selectId).text();
            $.ajax({
                url: 'get_pred',
                type: 'POST',
                data: data,
                success: function (data) {
                    $('#co').text(data.co.toFixed(2));
                    $('#no').text(data.no.toFixed(2));
                    $('#no2').text(data.no2.toFixed(2));
                    $('#pm10').text(data.mp10.toFixed(2));
                    $('#pm25').text(data.mp25.toFixed(2));
                }
            });
        }
    });


    let document_ht = window.innerHeight;
    let map_ht = document_ht - 100 - 48;
    $('#map').css('height', map_ht);
    $('.weather-maps__timeline').css('bottom', 100);
    var apiKey = "c053d5ae05234ab2a5b1adb9d9157932"; // Your BreezoMeter API key
    var mapBoxAccessToken = "pk.eyJ1IjoiZndlZHNmIiwiYSI6ImNrdW51eHU1ZzFyMjAycHJ2cHR1b3lqOGcifQ.gI7aoa75R-B_PY9sKSdNlQ"; // your mapbox access token from: https://account.mapbox.com
    mapboxgl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.1.0/mapbox-gl-rtl-text.js');
    var apiWeather = "ae17c1629fb9da40f8c0793a99083918";
    var errorMessageBrz =
        "Update the variable 'apiKey' with a BreezoMeter API key to see the tiles. Contact BreezoMeter if you need any help:    breezometer.com/contact-us";
    var errorMessageMapbox =
        "Update the variable 'mapBoxAccessToken' with a Mapbox Access Token to initialize the Mapbox SDK. You can get it from:                https://account.mapbox.com";

    if (apiKey === "") alert(errorMessageBrz);
    if (mapBoxAccessToken === "") alert(errorMessageMapbox);
    var map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v11", // your stylesheet location
        center: [37.623856, 55.751574], // starting position [lng, lat]
        zoom: 10, // starting zoom
        pitch: 45,
        doubleClickZoom: false,
        bearing: 0,
        accessToken: mapBoxAccessToken
    });

    var nav = new mapboxgl.NavigationControl({
        showCompass: true,
        showZoom: true
    });
    const language = new MapboxLanguage();
    map.addControl(language);

    map.addControl(nav, 'bottom-right');

    map.addControl(new mapboxgl.FullscreenControl(), 'bottom-left'); // full screen

    map.on('load', function () {
        addRasterSource();
        addRasterLayer();

    });

    function addRasterSource() {
        map.addSource("breezometer-tiles", {
            type: "raster",
            tiles: [
                `https://tiles.breezometer.com/v1/air-quality/breezometer-aqi/current-conditions/{z}/{x}/{y}.png?key=${apiKey}&breezometer_aqi_color=indiper`
            ],
            tileSize: 256,
            maxzoom: 12
        });
    }

    function addRasterLayer() {
        map.addLayer(
            {
                id: "breez",
                type: "raster",
                source: "breezometer-tiles",
                minzoom: 0,
                maxzoom: 22,
                paint: {
                    "raster-opacity": 0.6
                }
            },
            "admin-1-boundary-bg"
        );
    }

    map.on('dblclick', function (e) {
        var now = new Date();
        now.setMinutes(now.getMinutes() + (selectId + 1) * 20);
        now.setMinutes(0, 0, 0);
        console.log(DateFormat.format.date(now, 'yyyy-MM-ddTHH:mm:ss'));
        const coord = [e.lngLat.lng, e.lngLat.lat];
        $.ajax({
            url: `https://api.breezometer.com/air-quality/v2/forecast/hourly?lat=${e.lngLat.lat}&lon=${e.lngLat.lng}&key=${apiKey}&datetime=${DateFormat.format.date(now, 'yyyy-MM-ddTHH:mm:ss')}&lang=ru`,
            type: 'GET',
            success: function (data) {
                new mapboxgl.Popup()
                    .setLngLat(coord)
                    .setHTML(`<h1>${data.data.indexes.baqi.aqi_display}%</h1><p>${data.data.indexes.baqi.dominant_pollutant}</p><p>${data.data.indexes.baqi.category}</p>`)
                    .addTo(map);
            }
        });
    });

    for (const {geometry, properties} of tower.features) {
        let el = document.createElement('div');
        if (properties.id == 11) {
            el.className = 'marker station activation';
        } else {
            el.className = 'marker station';
        }
        el.id = properties.id;
        new mapboxgl.Marker(el).setLngLat(geometry.coordinates).addTo(map);
    }
    $('.station').click(function () {
        $('#' + data['id']).removeClass('activation');
        $('#' + $(this).attr('id')).addClass('activation');
        data['id'] = $(this).attr('id');
        data['name'] = $('#timeline_id_' + selectId).text();
        $.ajax({
            url: 'get_pred',
            type: 'POST',
            data: data,
            success: function (data) {
                $('#co').text(data.co.toFixed(2));
                $('#no').text(data.no.toFixed(2));
                $('#no2').text(data.no2.toFixed(2));
                $('#pm10').text(data.mp10.toFixed(2));
                $('#pm25').text(data.mp25.toFixed(2));
            }
        });
    });
});
