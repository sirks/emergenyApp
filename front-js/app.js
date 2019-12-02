const chars = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM';

function makeid(length) {
  let result = '';
  let charactersLength = chars.length;
  for (let _ = 0; _ < length; _++) {
    result += chars.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;

}

function getMyId() {
  let myid = window.localStorage.getItem('myid');
  if (myid) {
    return myid
  }
  myid = makeid(20);
  window.localStorage.setItem('myid', myid);
  return myid;
}

const myId = getMyId();

let mymap = L.map('map').setView([0, 0], 10);

L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw')
.addTo(mymap);


var myLocationIcon = L.icon({
  iconUrl: 'assets/blue.png',
  iconAnchor: [10, 10],
});

var otherLocationIcon = L.icon({
  iconUrl: 'assets/red.png',
  iconAnchor: [10, 10],
});

let myLocationMarker = undefined;
const mySosses = {};

updateLocation();

function updateLocation() {
  if (!navigator.geolocation) {
    console.log('no geolocation available!');
    return;
  }
  navigator.geolocation.getCurrentPosition(manageLocation);
  setTimeout(updateLocation, 9999)
}


function manageLocation(position) {
  const myLocation = [position.coords.latitude, position.coords.longitude];
  console.log(`new location ${myLocation}`);
  if (myLocationMarker) {
    myLocationMarker = L.marker(myLocation).update(myLocationMarker);
  } else {
    mymap.setView(myLocation, 10);
    myLocationMarker = L.marker(myLocation, {icon: myLocationIcon}).addTo(mymap);
  }

  manageSosses(myLocation)
}

updatePolygons();

function updatePolygons() {
  if (!navigator.geolocation) {
    console.log('no geolocation available!');
    return;
  }
  navigator.geolocation.getCurrentPosition(managePolygons);
  setTimeout(updatePolygons, 999999)
}

function managePolygons(position) {
  fetch(`https://${location.hostname}:5000/api/polygons?lat=${position.coords.latitude}&lon=${position.coords.longitude}`)
  .then(resp => resp.json())
  .then(json => drawPolygons(json))
  .catch(console.log)
}

function drawPolygons(polygons) {
  console.log(`drawing ${polygons}`);
  if (!polygons) {
    return;
  }
  Object.values(polygons).forEach(p => L.polygon(p.poldata, {
      color: 'red',
      fillColor: '#f03',
    }
    ).addTo(mymap).bindPopup("Hazard here")
  );
}

function sos() {
  navigator.geolocation.getCurrentPosition(saveSos);
}

function saveSos(position) {
  fetch(`https://${location.hostname}:5000/api/sos/?id=${myId}&lat=${position.coords.latitude}&lon=${position.coords.longitude}`)
  .catch(console.log)
}


function manageSosses(myLocation) {
  fetch(`https://${location.hostname}:5000/api/sosses/?id=${myId}&lat=${myLocation[0]}&lon=${myLocation[1]}`)
  .then(resp => resp.json())
  .then(json => drawSosses(json))
  .catch(console.log)
}

function drawSosses(sosses) {
  console.log(`drawing ${sosses}`);
  if (!sosses) {
    return;
  }
  let current_ids = Object.keys(mySosses);
  Object.entries(sosses).forEach(sos => {
    // debugger;
    if (current_ids.includes(sos[0])) {
      console.log(`update ${sos[0]}-${sos[1]}`);
      mySosses[sos[0]].setLatLng(sos[1]).update();
      current_ids.pop(sos[0])
    } else {
      console.log(`create ${sos[0]}-${sos[1]}`);
      mySosses[sos[0]] = L.marker(sos[1], {icon: otherLocationIcon}).addTo(mymap);
    }
  });
  current_ids.forEach(id => {
    console.log(`removing ${id}`);
    mySosses[id].remove();
    delete mySosses[1]
  });
}
