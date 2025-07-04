import qs from "qs";
import { apiClient } from "./apiClient";
import { Params, Receipt, User } from "@/types";

function printStatus(status: number) {
    switch (status) {
        case 201:
            console.log("Created!");
            break;
        case 202:
            console.log("Accepted!");
            break;
        case 203:
            console.log("Non-authoritative information!");
            break;
        case 204:
            console.log("No content!");
            break;
        case 400:
            console.error("Bad request!");
            throw new Error("Bad request!");
        case 401:
            console.error("Unauthorized!");
            // throw new Error("Unauthorized!");
            break;
        case 403:
            console.error("Forbidden!");
            throw new Error("Forbidden!");
        case 404:
            console.error("Not found!");
            throw new Error("Not found!");
        case 500:
            console.error("Internal server error!");
            throw new Error("Internal server error!");
        default:
            console.error("Unknown status!");
            throw new Error("Unknown status!");
    }
}

export const fetchGetMe = async () => {
    try {
        const response = await apiClient.get(`/auth/users/me/`);
        if (response.status === 200) {
            return response.data;
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.error("Błąd podczas pobierania danych użytkownika:", error);
        throw error;
    }
};

export const fetchPutMe = async (
    data: Partial<Pick<User, "email" | "avatar">>
) => {
    try {
        const response = await apiClient.put(`/auth/users/me/`, data);
        if (response.status === 200) {
            return response.data;
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.error("Błąd podczas aktualizacji danych użytkownika:", error);
        throw error;
    }
};

export const fetchDeleteMe = async (password: string) => {
    const response = await apiClient.delete("/auth/users/me/", {
        data: { current_password: password },
    });
    if (response.status === 204) {
        return true;
    } else {
        printStatus(response.status);
    }
};

export const fetchGetReceipts = async (params?: Params) => {
    try {
        const response = await apiClient.get(`/api/receipts/`, {
            params: params,
            paramsSerializer: (params) => {
                return qs.stringify(params, { arrayFormat: "comma" });
            },
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

export const fetchGetReceiptsByID = async (params: {
    id: number | number[];
}) => {
    if (!Array.isArray(params.id)) params.id = Array(params.id);
    if (!params.id || params.id.length === 0) return [];

    try {
        // Wykonujemy zapytanie dla każdego ID w pętli asynchronicznie
        const responses = await Promise.all(
            params.id.map(async (receiptId) => {
                const response = await apiClient.get(
                    `/api/receipts/${receiptId}/`
                );
                return response.data;
            })
        );

        return responses; // Zwracamy listę paragonów
    } catch (error) {
        console.error(error);
        throw error;
    }
};

export const fetchPostReceipt = async (receipt: Receipt[]) => {
    // console.log(receipt);
    // console.log(JSON.stringify(receipt));
    try {
        const response = await apiClient.post(`/api/receipts/`, receipt);
        if (response.status === 201) {
            return response.data;
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.warn(JSON.stringify(receipt));
        console.error(error);
        throw error;
    }
};

export const fetchPutReceipt = async (receiptId: number, receipt: Receipt) => {
    // console.log(receipt);
    // console.log(JSON.stringify(receipt));
    try {
        const response = await apiClient.put(
            `/api/receipts/${receiptId}/`,
            receipt
        );
        if (response.status === 200) {
            return response.data;
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.warn(JSON.stringify(receipt));
        console.error(error);
        throw error;
    }
};

export const fetchDeleteReceipt = async (receipt: Receipt) => {
    try {
        const response = await apiClient.delete(`/api/receipts/${receipt.id}/`);
        if (response.status === 204) {
            return response.data;
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
};

export const fetchSearchRecentShops = async (query: string) => {
    try {
        // Jeśli query jest krótsze niż 3 litery, zwróć pustą tablicę
        if (query.length < 3) return [];

        // Wykonaj zapytanie do backendu
        const response = await apiClient.get(`/api/recent-shops/`, {
            params: { q: query },
        });

        // Jeśli zapytanie było udane, zwróć dane
        if (response.status === 200) {
            return response.data.results; // Zakładamy, że API zwraca pole `results`
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.error("Error fetching recent shops:", error);
        throw error;
    }
};

export const fetchItemPredictions = async (shop: string, query: string) => {
    try {
        // Jeśli query jest krótsze niż 3 litery, zwróć pustą tablicę
        if (query.length < 3) return [];

        // Wykonaj zapytanie do backendu
        const response = await apiClient.get(`/api/item-predictions/`, {
            params: { shop: shop, q: query },
        });

        // Jeśli zapytanie było udane, zwróć dane
        if (response.status === 200) {
            return response.data.results; // Zakładamy, że API zwraca pole `results`
        } else {
            printStatus(response.status);
        }
    } catch (error) {
        console.error("Error fetching recent shops:", error);
        throw error;
    }
};

export const fetchLineSums = async (params?: Params) => {
    try {
        const response = await apiClient.get(`/api/fetch/line-sums/`, {
            params: params,
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

export const fetchBarShops = async (params?: Params) => {
    try {
        const response = await apiClient.get(`/api/fetch/bar-shops/`, {
            params: params,
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

export const fetchPieCategories = async (params?: Params) => {
    try {
        const response = await apiClient.get(`/api/fetch/pie-categories/`, {
            params: params,
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
