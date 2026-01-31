import axios from "axios";
import { getToken } from "../utils/auth";

const BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({ baseURL: BASE_URL });

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const signup = (data) => api.post("/auth/signup", data);
export const login = (data) => api.post("/auth/login", data);
export const getMe = () => api.get("/auth/me");
export const getSignals = (paid = false) => api.get(`/signals?paid=${paid}`);
export const createCheckout = () => api.post("/billing/create-checkout");
export const checkBillingStatus = () => api.get("/billing/status");
