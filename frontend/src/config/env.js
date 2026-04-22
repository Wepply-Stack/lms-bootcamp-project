const env = {
  API_URL: import.meta.env.VITE_API_URL,
  APP_NAME: import.meta.env.VITE_APP_NAME,
  TIMEOUT: Number(import.meta.env.VITE_API_TIMEOUT) || 5000,
  DEBUG: import.meta.env.VITE_DEBUG === "true",

  // Built-in Vite flags
  MODE: import.meta.env.MODE,
  IS_DEV: import.meta.env.DEV,
  IS_PROD: import.meta.env.PROD,
};

export default env;