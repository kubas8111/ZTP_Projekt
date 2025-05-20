// src/api/apiClient.ts
import axios, {
    AxiosError,
    AxiosResponse,
    InternalAxiosRequestConfig,
} from "axios";
import {
    getAccessToken,
    setAccessToken,
    getRefreshToken,
    clearTokens,
} from "@/lib/token-storage";

export const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_ENDPOINT ?? "http://localhost:8000",
    withCredentials: true, // jeśli backend ustawia też cookies
});

apiClient.interceptors.request.use((config) => {
    const token = getAccessToken();
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

let isRefreshing = false;
let queue: Array<(token: string | null) => void> = [];

const resolveQueue = (token: string | null) => {
    queue.forEach((cb) => cb(token));
    queue = [];
};

apiClient.interceptors.response.use(
    (response: AxiosResponse) => response, // 2xx? – zwracamy dalej
    async (error: AxiosError) => {
        const original = error.config as
            | (InternalAxiosRequestConfig & { _retry?: boolean })
            | undefined;

        // brak odpowiedzi lub już po próbie refreshu
        if (!error.response || !original || original._retry) {
            return Promise.reject(error);
        }

        // obsługujemy tylko 401
        if (error.response.status !== 401) return Promise.reject(error);
        original._retry = true;

        if (isRefreshing) {
            return new Promise((resolve, reject) => {
                queue.push((token) => {
                    if (token) {
                        original.headers.Authorization = `Bearer ${token}`;
                        resolve(apiClient(original));
                    } else {
                        reject(error);
                    }
                });
            });
        }

        isRefreshing = true;
        try {
            const refresh = getRefreshToken();
            if (!refresh) throw new Error("No refresh token");

            const { data } = await axios.post(
                "/auth/jwt/refresh/",
                { refresh },
                { baseURL: apiClient.defaults.baseURL }
            );

            setAccessToken(data.access);
            resolveQueue(data.access);

            original.headers.Authorization = `Bearer ${data.access}`;
            return apiClient(original); // ponów pierwotne żądanie
        } catch (refreshErr) {
            clearTokens(); // refresh nie zadziałał → wyloguj
            resolveQueue(null);
            return Promise.reject(refreshErr);
        } finally {
            isRefreshing = false;
        }
    }
);

export default apiClient;
