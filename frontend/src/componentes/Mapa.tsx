import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from "react-leaflet";
import { useEffect, useState } from "react";

export default function Mapa({ stations, statesSaturation }: any) {
  const [statesData, setStatesData] = useState<any>(null);

  useEffect(() => {
    if (statesSaturation && statesSaturation.length > 0) {
      // Convert to GeoJSON FeatureCollection
      const geoJson = {
        type: "FeatureCollection",
        features: statesSaturation.map((state: any) => ({
          type: "Feature",
          properties: { name: state.state, saturation: state.saturation },
          geometry: state.geometry
        }))
      };
      setStatesData(geoJson);
    }
  }, [statesSaturation]);

  const onEachFeature = (feature: any, layer: any) => {
    layer.bindPopup(`<b>${feature.properties.name}</b><br/>Saturación: ${feature.properties.saturation} estaciones`);
  };

  return (
    <MapContainer
      center={[19.43, -99.13]} // CDMX
      zoom={5}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* {statesData && (
        <GeoJSON 
          data={statesData} 
          style={styleFunction}
          onEachFeature={onEachFeature} 
        />
      )} */}

      {stations.map((s: any, i: number) => {
        if (!s.lat || !s.lon) return null;

        return (
          <Marker key={i} position={[Number(s.lat), Number(s.lon)]}>
            <Popup>
              <strong>{s.name}</strong><br />
              Estado: {s.state}<br />
              Precio: ${s.price}
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}