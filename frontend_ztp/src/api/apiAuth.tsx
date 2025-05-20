import { apiClient } from "./apiClient";

export const fetchPostLogin = async (username: string, password: string) => {
    try {
        const response = await apiClient.post("/auth/jwt/create/", {
            username,
            password,
        });

        if (response.status === 200) {
            return response.data;
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
};

export const fetchPostRefresh = async (refresh: string) => {
    try {
        const response = await apiClient.post("/auth/jwt/refresh/", {
            refresh,
        });

        if (response.status === 200) {
            return response.data as { access: string };
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
};

export const fetchPostVerify = async (token: string) => {
    try {
        const response = await apiClient.post("/auth/jwt/verify/", { token });

        if (response.status === 200) {
            /* Zwraca pustą odpowiedź { } przy poprawnym tokenie */
            return true;
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
};

export const fetchPostRegister = async (
    email: string,
    username: string,
    password: string
) => {
    try {
        const response = await apiClient.post("/auth/users/", {
            email,
            username,
            password,
        });

        if (response.status === 201) {
            /* backend zwraca obiekt użytkownika (bez hasła) */
            return response.data;
        } else {
            printStatus(response.status);
        }
    } catch (error: any) {
        /* Przy błędzie walidacji Djoser zwraca 400 + szczegóły w response.data */
        console.error(error?.response?.data || error);
        throw error;
    }
};
function printStatus(status: number) {
    throw new Error(`Function not implemented. ${status}`);
}
