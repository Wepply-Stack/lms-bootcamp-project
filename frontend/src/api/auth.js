import axiosInstance from "./axiosInstance";

export const loginUser = async (credentials) => {
  const response = await axiosInstance.post("/login/", credentials);
  return response.data;
};

export const logoutUser = async () => {
  await axiosInstance.post("/logout/");
};
