const API_BASE = "http://localhost:4000/api";

export const getStations = async (limit = 200, offset = 0) => {
  try {
    const response = await fetch(`${API_BASE}/stations?limit=${limit}&offset=${offset}`);
    if (!response.ok) throw new Error("Error al obtener estaciones");
    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return [];
  }
};

export const getPrices = async () => {
  try {
    const response = await fetch(`${API_BASE}/prices`);
    if (!response.ok) throw new Error("Error al obtener precios");
    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return [];
  }
};

export const getPlaces = async () => {
  try {
    const response = await fetch(`${API_BASE}/places`);
    if (!response.ok) throw new Error("Error al obtener lugares");
    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return [];
  }
};

export const get_states_saturation = async () => {
  try {
    const response = await fetch(`${API_BASE}/states-saturation`);
    if (!response.ok) throw new Error("Error al obtener saturación por estados");
    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return [];
  }
};

export const getTopNeighboringStations = async () => {
  try {
    const response = await fetch(`${API_BASE}/top-neighboring-stations`);
    if (!response.ok) throw new Error("Error al obtener estaciones vecinas");
    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return [];
  }
};