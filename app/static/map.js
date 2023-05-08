/* 
    The object is a spot location (latitude + longitude obtained by requesting here.com API) and the html div where
the map will be display.
    The 2 methods implements here.com geocoding API to obtain a map and to mark the location
*/

'use strict';

class Map {

    constructor(latitude, longitude, html_div) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.html_div = html_div;
    }

    platform_map_type(apikey) {
        this.platform = new H.service.Platform({
            'apikey': apikey});
        this.default_layers = this.platform.createDefaultLayers();
        }

    display_map() {
        if (this.latitude != -1) {
            new H.Map(
                this.html_div,
                this.default_layers.vector.normal.map,
                {
                    zoom: 10,
                    center: { lat: this.latitude, lng: this.longitude}
                })
                .addObject(new H.map.Marker({lat: this.latitude, lng: this.longitude},
                                            {icon: new H.map.Icon('/static/map_marker.png')}));
        }
    }
}