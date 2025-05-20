import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "@/components/theme-provider";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GlobalProvider } from "@/context/GlobalContext";
import Layout from "@/pages/layout";
import { AuthProvider } from "@/context/AuthContext";
import Login from "@/pages/login";
import Register from "@/pages/register";
import PrivateRoute from "@/routes/private-route";

// Komponent Home jest importowany statycznie
import Home from "@/pages/home";

// Pozostałe strony ładujemy dynamicznie
const Expenses = lazy(() => import("@/pages/expenses"));
const Income = lazy(() => import("@/pages/income"));
const Summary = lazy(() => import("@/pages/summary"));
const Settings = lazy(() => import("@/pages/settings"));

function App() {
    const queryClient = new QueryClient();

    return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <QueryClientProvider client={queryClient}>
                <AuthProvider>
                    <GlobalProvider>
                        <BrowserRouter>
                            <Layout>
                                <Routes>
                                    <Route path="/login" element={<Login />} />
                                    <Route
                                        path="/register"
                                        element={<Register />}
                                    />
                                    <Route element={<PrivateRoute />}>
                                        <Route path="/" element={<Home />} />
                                        <Route
                                            path="/expenses"
                                            element={
                                                <Suspense
                                                    fallback={
                                                        <div>Ładowanie...</div>
                                                    }>
                                                    <Expenses />
                                                </Suspense>
                                            }
                                        />
                                        <Route
                                            path="/income"
                                            element={
                                                <Suspense
                                                    fallback={
                                                        <div>Ładowanie...</div>
                                                    }>
                                                    <Income />
                                                </Suspense>
                                            }
                                        />
                                        <Route
                                            path="/summary"
                                            element={
                                                <Suspense
                                                    fallback={
                                                        <div>Ładowanie...</div>
                                                    }>
                                                    <Summary />
                                                </Suspense>
                                            }
                                        />

                                        <Route
                                            path="/settings"
                                            element={
                                                <Suspense
                                                    fallback={
                                                        <div>Ładowanie...</div>
                                                    }>
                                                    <Settings />
                                                </Suspense>
                                            }
                                        />
                                    </Route>
                                </Routes>
                            </Layout>
                        </BrowserRouter>
                    </GlobalProvider>
                </AuthProvider>
            </QueryClientProvider>
        </ThemeProvider>
    );
}

export default App;
