import axiosInstance, { setAccessToken } from "./axiosInstance";

export const loginUser = async (credentials) => {
  const response = await axiosInstance.post("/login/", credentials);

  const { access } = response.data;

  setAccessToken(access);

  return response.data;
};

export const logoutUser = async () => {
  await axiosInstance.post("/logout/");
  setAccessToken(null);
};
