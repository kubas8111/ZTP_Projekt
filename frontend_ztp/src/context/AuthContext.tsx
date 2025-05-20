import { createContext, useState, useContext, ReactNode } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchPostLogin, fetchPostRegister } from "@/api/apiAuth";
import { JwtPair } from "@/types";
import { z, ZodError } from "zod";
import { setAccessToken, setRefreshToken } from "@/lib/token-storage";

const loginSchema = z.object({
    username: z.string().min(3, "Nazwa użytkownika musi mieć ≥ 3 znaki"),
    password: z.string().min(6, "Hasło musi mieć ≥ 6 znaków"),
});

const registerSchema = z
    .object({
        email: z.string().email("Niepoprawny email"),
        username: z.string().min(3, "Nazwa użytkownika musi mieć ≥ 3 znaki"),
        password: z.string().min(6, "Hasło musi mieć ≥ 6 znaków"),
        re_password: z.string().min(6),
    })
    .refine((d) => d.password === d.re_password, {
        path: ["re_password"],
        message: "Hasła nie są identyczne",
    });

type LoginPayload = z.infer<typeof loginSchema>;
type RegisterPayload = z.infer<typeof registerSchema>;

interface AuthState {
    userUsername: string | null;
    login: (username: string, password: string) => Promise<JwtPair>;
    logout: () => void;
    register: (payload: RegisterPayload) => Promise<void>;
}

const AuthContext = createContext<AuthState>({} as AuthState);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [userUsername, setUsername] = useState<string | null>(
        localStorage.getItem("username")
    );
    const qc = useQueryClient();

    const loginMut = useMutation<JwtPair, Error, LoginPayload>({
        mutationFn: async (payload) => {
            loginSchema.parse(payload);
            return fetchPostLogin(payload.username, payload.password);
        },

        onSuccess: ({ access, refresh }, { username }) => {
            setAccessToken(access); // Ustawienie tokenu w localStorage
            setRefreshToken(refresh); // Ustawienie tokenu odświeżającego w localStorage
            localStorage.setItem("username", username);
            setUsername(username);

            qc.invalidateQueries({ queryKey: ["currentUser"] });
        },

        onError: (err) => {
            if (err instanceof ZodError) {
                console.error("Błąd walidacji:", err.flatten().fieldErrors);
            } else {
                console.error(err.message);
            }
        },
    });

    const registerMut = useMutation<void, Error, RegisterPayload>({
        mutationFn: async (payload) => {
            registerSchema.parse(payload);

            await fetchPostRegister(
                payload.email,
                payload.username,
                payload.password
            );
        },

        onSuccess: async (_void, { username, password }) => {
            await loginMut.mutateAsync({ username, password });
        },

        onError: (err) => {
            if (err instanceof ZodError) {
                console.error("Błąd walidacji:", err.flatten().fieldErrors);
            } else {
                console.error(err.message);
            }
        },
    });

    const logout = () => {
        localStorage.clear();
        setUsername(null);
        qc.clear();
    };

    return (
        <AuthContext.Provider
            value={{
                userUsername,
                login: (username, password) =>
                    loginMut.mutateAsync({ username, password }),
                logout,
                register: (payload) => registerMut.mutateAsync(payload),
            }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
