export type User = {
    id: number;
    username: string;
    email: string;
    avatar?: string;
};

export type Item = {
    id: number;
    category: string;
    value: string;
    description: string;
    quantity: number;
};

export type Receipt = {
    id: number;
    payment_date: string;
    shop: string;
    transaction_type: string;
    items: Item[];
};

export type Params = {
    id?: number;
    month?: number;
    year?: number;
    category?: string[];
    transaction_type?: string;
};

export type Shops = {
    id?: number;
    name: string;
};

export type JwtPair = {
    access: string;
    refresh: string;
};
