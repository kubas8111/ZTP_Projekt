// src/utils/tokenStorage.ts
export const getAccessToken = () => localStorage.getItem("access");
export const setAccessToken = (t: string) => localStorage.setItem("access", t);

export const getRefreshToken = () => localStorage.getItem("refresh");
export const setRefreshToken = (t: string) =>
    localStorage.setItem("refresh", t);

export const clearTokens = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
};
