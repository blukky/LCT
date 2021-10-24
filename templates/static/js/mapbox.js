var apiKey = "c8b395eabd944d97b69dac009681f732"; // Your BreezoMeter API key
var mapBoxAccessToken = "pk.eyJ1IjoiZndlZHNmIiwiYSI6ImNrdW51eHU1ZzFyMjAycHJ2cHR1b3lqOGcifQ.gI7aoa75R-B_PY9sKSdNlQ"; // your mapbox access token from: https://account.mapbox.com

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
    accessToken: mapBoxAccessToken
});

map.on("load", function () {
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
            id: "breezometer-tiles",
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