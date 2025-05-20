import React, { createContext, useContext, useState, ReactNode } from "react";
import { Params, Receipt, Shops } from "@/types";

interface GlobalState {
    receipts: Receipt[];
    setReceipts: (receipts: Receipt[]) => void;

    shops: Shops[];
    setShops: (shops: Shops[]) => void;

    summaryFilters: Params;
    setSummaryFilters: (
        params: Params | ((prevFilters: Params) => Params)
    ) => void;
}

// Domyślny stan
const defaultState: GlobalState = {
    receipts: [],
    setReceipts: () => {},
    shops: [],
    setShops: () => {},
    summaryFilters: {
        month: 0,
        year: 0,
        category: [],
    },
    setSummaryFilters: () => {},
};

// Tworzenie kontekstu
const GlobalContext = createContext<GlobalState>(defaultState);

// Provider dla aplikacji
export const GlobalProvider: React.FC<{ children: ReactNode }> = ({
    children,
}) => {
    const [receipts, setReceipts] = useState<Receipt[]>([]);
    const [shops, setShops] = useState<Shops[]>([]);
    const [summaryFilters, setSummaryFilters] = useState<Params>({
        month: new Date().getMonth() + 1,
        year: new Date().getFullYear(),
        category: [],
    });

    return (
        <GlobalContext.Provider
            value={{
                receipts,
                setReceipts,
                shops,
                setShops,
                summaryFilters,
                setSummaryFilters,
            }}>
            {children}
        </GlobalContext.Provider>
    );
};

// Hook do korzystania z GlobalContext
export const useGlobalContext = () => useContext(GlobalContext);
