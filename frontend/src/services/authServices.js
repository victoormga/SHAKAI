import api from "./api";

export async function loginService(email, password) {
  const res = await api.post("/auth/login/", { email, password });
  return res.data; // { access, refresh }
}

export async function registerService(display_name, email, password) {
  const res = await api.post("/auth/register/", {
    display_name,
    email,
    password,
  });
  return res.data;
}

export async function logoutService(refresh) {
  return api.post("/auth/logout/", { refresh });
}

export async function fetchMyProfile() {
  return api.get("/auth/me/");
}

export async function updateProfileService(formData) {
  // Se envía FormData para multipart (imagen)
  return api.patch("/auth/me/profile/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
}