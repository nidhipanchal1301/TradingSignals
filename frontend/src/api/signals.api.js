import api from "./axios";

export const getSignals = (paid) =>
  api.get(`/signals?paid=${paid}`);
