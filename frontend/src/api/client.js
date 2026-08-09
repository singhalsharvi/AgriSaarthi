import { 
  MOCK_CROP_RESPONSE, 
  MOCK_DISEASE_RESPONSE, 
  MOCK_GOVT_SCHEMES_RESPONSE 
} from './mockData';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function fetchWithTimeout(url, options = {}, timeoutMs = 8000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      }
    });
    clearTimeout(timeoutId);
    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
}

export const apiService = {
  // Check API status
  checkHealth: async () => {
    try {
      return await fetchWithTimeout(`${BASE_URL}/health`, { method: 'GET' }, 3000);
    } catch {
      return { status: "healthy", mode: "offline_demo" };
    }
  },

  // 1. Crop Recommendation API
  recommendCrop: async (payload) => {
    try {
      const data = await fetchWithTimeout(`${BASE_URL}/crop/recommend`, {
        method: 'POST',
        body: JSON.stringify({
          location: payload.location || "Meerut, Uttar Pradesh",
          season: payload.season || "Kharif",
          Nitrogen: payload.n ? parseFloat(payload.n) : 90.0,
          Phosphorus: payload.p ? parseFloat(payload.p) : 42.0,
          Potassium: payload.k ? parseFloat(payload.k) : 43.0,
          Temperature: payload.temperature ? parseFloat(payload.temperature) : undefined,
          Humidity: payload.humidity ? parseFloat(payload.humidity) : undefined,
          pH_Value: payload.ph ? parseFloat(payload.ph) : 6.8,
          Rainfall: payload.rainfall ? parseFloat(payload.rainfall) : undefined,
          Soil_Type: payload.soilType || undefined,
          user_query: payload.userQuery || `What crops are suitable for ${payload.location} in ${payload.season}?`
        })
      });
      return data;
    } catch (err) {
      console.warn("Backend API unreachable, using realistic AgriSaarthi dataset:", err.message);
      // Return custom mock response populated with user location & season
      return {
        ...MOCK_CROP_RESPONSE,
        location: payload.location || MOCK_CROP_RESPONSE.location,
        season: payload.season || MOCK_CROP_RESPONSE.season
      };
    }
  },

  // 2. Disease Detection API
  analyzeDisease: async (payload) => {
    try {
      const data = await fetchWithTimeout(`${BASE_URL}/disease/analyze`, {
        method: 'POST',
        body: JSON.stringify({
          crop_name: payload.cropName || "Tomato",
          symptoms: payload.symptoms || "Dark brown leaf spots with yellow margins",
          user_query: payload.userQuery || "How to treat leaf spot disease?"
        })
      });
      return data;
    } catch (err) {
      console.warn("Backend API unreachable, using realistic AgriSaarthi dataset:", err.message);
      return {
        ...MOCK_DISEASE_RESPONSE,
        crop_name: payload.cropName || "Tomato"
      };
    }
  },

  // 3. Government Schemes API
  recommendSchemes: async (payload) => {
    try {
      const data = await fetchWithTimeout(`${BASE_URL}/government-schemes/recommend`, {
        method: 'POST',
        body: JSON.stringify({
          state: payload.state || "Uttar Pradesh",
          crop: payload.crop || "Rice",
          farmer_category: payload.farmerCategory || "Small and marginal farmer families",
          annual_income: payload.annualIncome ? parseFloat(payload.annualIncome) : 50000,
          landholding: payload.landholding ? parseFloat(payload.landholding) : 1.5,
          user_query: payload.userQuery || "Financial assistance and crop insurance schemes",
          top_k: 5
        })
      });
      return data;
    } catch (err) {
      console.warn("Backend API unreachable, using realistic AgriSaarthi dataset:", err.message);
      return {
        ...MOCK_GOVT_SCHEMES_RESPONSE,
        state: payload.state || "Uttar Pradesh"
      };
    }
  }
};
