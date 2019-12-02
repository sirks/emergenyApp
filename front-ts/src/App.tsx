import React from 'react';
import './App.css';
import {TileLayer, Map} from "react-leaflet";
import {LatLngLiteral} from 'leaflet';


const position: LatLngLiteral = {lat: 60, lng: 24};

const App: React.FC = () => {
  return (
    <div className="App">
      <Map center={position} zoom={13}>
        <TileLayer
          attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw"
        />
      </Map>
    </div>
  );
};

export default App;
