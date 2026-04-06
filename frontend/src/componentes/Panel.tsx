import { useEffect, useState } from "react";
import { getStations, get_states_saturation, getTopNeighboringStations } from "../servicios/api";
import Mapa from "./Mapa"

export default function Dashboard() {
  const [stations, setStations] = useState<any[]>([]);
  const [page, setPage] = useState(0);
  const [hasMoreStations, setHasMoreStations] = useState(true);
  const [isLoadingStations, setIsLoadingStations] = useState(false);
  const [statesSaturation, setStatesSaturation] = useState<any[]>([]);
  const [topNeighbors, setTopNeighbors] = useState<any[]>([]);

  const fetchStations = async (pageNumber: number) => {
    setIsLoadingStations(true);
    const data: any = await getStations(200, pageNumber * 200);
    setStations((prev) => (pageNumber === 0 ? data : [...prev, ...data]));
    if (data.length < 200) {
      setHasMoreStations(false);
    }
    setIsLoadingStations(false);
  };

  useEffect(() => {
    fetchStations(0);
    get_states_saturation().then((data: any) => setStatesSaturation(data));
    getTopNeighboringStations().then((data: any) => setTopNeighbors(data));
  }, []);

  // Calcular rangos de precios por tipo de combustible
  const getPriceRanges = () => {
    const fuelTypes = ["diesel", "premium", "regular"];
    const ranges: any = {};
    
    fuelTypes.forEach(type => {
      const prices = stations
        .filter(s => s.fuel_type === type && s.price)
        .map(s => Number(s.price));
      
      if (prices.length > 0) {
        ranges[type] = {
          min: Math.min(...prices).toFixed(2),
          max: Math.max(...prices).toFixed(2)
        };
      }
    });
    
    return ranges;
  };

  const priceRanges = getPriceRanges();
  



  return (
    <div className="min-h-screen bg-white-100">
      
      {/* HEADER */}
      <header className="bg-white shadow px-6 py-4 flex justify-between items-center spacer-top-md">
        <h1 className="text-l font-bold">
         Gasolineras WalMart
        </h1>
      </header>

      {/* CONTENT */}
      <main className="p-6 space-y-6">

        <div className="bg-white rounded-2xl shadow p-4">
            <h2 className="text-xl font-semibold mb-4">
                Mapa de estaciones (Cargando por bloques de 200)
            </h2>

            <Mapa stations={stations} statesSaturation={statesSaturation} />

            <div className="mt-4 flex items-center gap-3">
              {hasMoreStations ? (
                <button
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  onClick={() => {
                    const nextPage = page + 1;
                    setPage(nextPage);
                    fetchStations(nextPage);
                  }}
                  disabled={isLoadingStations}
                >
                  {isLoadingStations ? "Cargando..." : "Cargar más estaciones"}
                </button>
              ) : (
                <span className="text-gray-500">No hay más estaciones para cargar.</span>
              )}
            </div>
          </div>
        {/* CARDS */}
        <div className="bg-white rounded-2xl shadow p-4">
           <h2 className="text-xl font-semibold mb-4">
            Rangos de Precios
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <StatCard className="back-green"
            title="Regular"
            value={priceRanges.regular ? `$${priceRanges.regular.min} - $${priceRanges.regular.max}` : "Sin datos"}
          />
          <StatCard className="back-red"
            title="Premium"
            value={priceRanges.premium ? `$${priceRanges.premium.min} - $${priceRanges.premium.max}` : "Sin datos"}
          />
          <StatCard className="back-black"
            title="Diesel"
            value={priceRanges.diesel ? `$${priceRanges.diesel.min} - $${priceRanges.diesel.max}` : "Sin datos"}
          />
        </div>
         {/* TABLA */}
        <div className="bg-white rounded-2xl shadow p-4 spacer-top-md">
          <h2 className="text-xl font-semibold mb-4">
            Saturación por estado (Top 10)
          </h2>
          
          <table className="w-full text-left">
            <thead>
              <tr className="border-b text-gray-600 text-sm">
                <th className="py-2">Estado</th>
                <th>Saturación</th>
              </tr>
            </thead>

            <tbody>
              {statesSaturation
                .sort((a, b) => b.saturation - a.saturation)
                .slice(0, 10)
                .map((s, i) => (
                <tr key={i} className="border-b hover:bg-gray-50">
                  <td className="py-2 font-medium">{s.state}</td>
                  <td>{s.saturation} estaciones</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* TOP 10 ESTACIONES CON MAS VECINOS */}
        <div className="bg-white rounded-2xl shadow p-4 spacer-top-md">
          <h2 className="text-xl font-semibold mb-4">
            Top 10 Estaciones con Más Vecinas (Dentro de 3 km)
          </h2>

          <table className="w-full text-left">
            <thead>
              <tr className="border-b text-gray-600 text-sm">
                <th className="py-2">Nombre</th>
                <th>Estaciones Vecinas (3 km)</th>
              </tr>
            </thead>

            <tbody>
              {topNeighbors.length > 0 ? (
                topNeighbors.map((s, i) => (
                  <tr key={i} className="border-b hover:bg-gray-50">
                    <td className="py-2 font-medium">{s.name}</td>
                    <td className="text-blue-600 font-semibold">
                      {s.neighbors_count} estaciones
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={2} className="py-4 text-center text-gray-500">
                    No se encontraron estaciones vecinas dentro de 3km.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        </div>
       


       

      </main>
    </div>
  );
}

/* COMPONENTE CARD */
function StatCard({ title, value, className }: any) {
  const isColored = className && (className.includes('back-') || className.includes('bg-'));
  return (
    <div className={`bg-white p-4 rounded-2xl shadow hover:shadow-lg transition ${className || ''}`}>
      <p className={`${isColored ? 'text-white' : 'text-gray-500'} text-sm`}>{title}</p>
      <h2 style={isColored ? { color: 'white' } : {}} className="text-2xl font-bold mt-2">{value}</h2>
    </div>
  );
}