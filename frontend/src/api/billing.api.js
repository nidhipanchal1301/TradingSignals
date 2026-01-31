import axios from "./axios";

export const createCheckout = () => {
  return axios.post("/billing/create-checkout");
};

export const getBillingStatus = () => {
  return axios.get("/billing/status");
};
