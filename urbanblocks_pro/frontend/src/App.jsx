import React, { useState, useRef } from "react";
import axios from "axios";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import Plot from "react-plotly.js";
import L from "leaflet";

export default function App() {
  const [fileInputs, setFileInputs] = useState({});
  const [filename, setFilename] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [geojson, setGeojson] = useState(null);
  const [error, setError] = useState("");
  const geoJsonLayerRef = useRef();

  const handleFileChange = (e) => {
    setFileInputs({ ...fileInputs, [e.target.name]: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setGeojson(null);
    setError("");
    const formData = new FormData();
    ["shp", "shx", "dbf", "prj"].forEach((ext) => {
      if (fileInputs[ext]) formData.append(ext, fileInputs[ext]);
    });
    formData.append("filename", filename);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/upload-shapefile/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);

      // Fetch the GeoJSON file from backend if upload is successful
      if (res.data.geojson_path) {
        const geojsonRes = await axios.get(
          `http://127.0.0.1:8000/${res.data.geojson_path.replace(/\\/g, "/")}`
        );
        setGeojson(geojsonRes.data);
      }
    } catch (err) {
      setError(err?.response?.data?.message || err.message || "Unknown error");
      setResult({ status: "error", message: err.message });
    }
    setLoading(false);
  };

  // Color palette for wards
  const colors = [
    "#2563eb", "#059669", "#f59e42", "#e11d48", "#a21caf", "#facc15", "#0ea5e9", "#16a34a"
  ];
  const getColor = (name) => {
    // Assign a color based on the zone/ward name
    if (!name) return "#888";
    let hash = 0;
    for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
    return colors[Math.abs(hash) % colors.length];
  };

  // Style each polygon
  const onEachFeature = (feature, layer) => {
    const name = feature.properties?.ZoneName || feature.properties?.zone_type || feature.properties?.ZoneCode || "Unknown";
    layer.bindPopup(`<b>${name}</b>`);
    layer.setStyle({
      color: "#222",
      weight: 1,
      fillColor: getColor(name),
      fillOpacity: 0.5,
    });
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-2xl font-bold mb-4 text-blue-700">UrbanBlocks Shapefile Uploader</h1>
      <form className="bg-white p-6 rounded shadow space-y-4 w-full max-w-md" onSubmit={handleSubmit}>
        <input
          className="border p-2 w-full"
          type="text"
          placeholder="Filename"
          value={filename}
          onChange={(e) => setFilename(e.target.value)}
          required
        />
        {["shp", "shx", "dbf", "prj"].map((ext) => (
          <div key={ext}>
            <label className="block mb-1 font-medium">{ext.toUpperCase()} file</label>
            <input
              className="border p-2 w-full"
              type="file"
              name={ext}
              accept={`.${ext}`}
              onChange={handleFileChange}
              required
            />
          </div>
        ))}
        <button
          className={`bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full ${loading ? "opacity-60 cursor-not-allowed" : ""}`}
          type="submit"
          disabled={loading}
        >
          {loading ? "Uploading..." : "Upload"}
        </button>
        {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
      </form>

      {result && (
        <div className="mt-6 w-full max-w-xl bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Backend Response</h2>
          <pre className="text-sm bg-gray-50 p-2 rounded">{JSON.stringify(result, null, 2)}</pre>
          {result.zone_info && result.zone_info.zone_summary && (
            <div className="mt-4">
              <h2 className="text-lg font-semibold mb-2">Zone Summary</h2>
              <Plot
                data={[
                  {
                    type: "bar",
                    x: Object.keys(result.zone_info.zone_summary),
                    y: Object.values(result.zone_info.zone_summary),
                    marker: { color: Object.keys(result.zone_info.zone_summary).map(getColor) },
                  },
                ]}
                layout={{
                  width: 400,
                  height: 300,
                  title: "Zones Count",
                  xaxis: { title: "Zone Name" },
                  yaxis: { title: "Count" },
                  margin: { t: 40, l: 40, r: 20, b: 80 },
                }}
              />
            </div>
          )}
        </div>
      )}

      {geojson && (
        <div className="mt-6 w-full max-w-2xl bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Ward Map</h2>
          <MapContainer
            style={{ height: "400px", width: "100%" }}
            center={[12.9716, 77.5946]} // Center on Bengaluru
            zoom={11}
            scrollWheelZoom={true}
          >
            <TileLayer
              attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <GeoJSON
              data={geojson}
              onEachFeature={onEachFeature}
              ref={geoJsonLayerRef}
            />
          </MapContainer>
          <div className="text-xs text-gray-500 mt-2">
            <b>Tip:</b> Click on a ward to see its name.
          </div>
        </div>
      )}
    </div>
  );
}