import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "@/components/theme-provider";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GlobalProvider } from "@/context/GlobalContext";
import Layout from "@/pages/layout";

// Komponent Home jest importowany statycznie
import Home from "@/pages/home";

// Pozostałe strony ładujemy dynamicznie
const Expenses = lazy(() => import("@/pages/expenses"));
const Income = lazy(() => import("@/pages/income"));
const Settings = lazy(() => import("@/pages/settings"));

function App() {
    const queryClient = new QueryClient();

    return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <QueryClientProvider client={queryClient}>
                <GlobalProvider>
                    <BrowserRouter>
                        <Layout>
                            <Routes>
                                <Route path="/" element={<Home />} />
                                <Route
                                    path="/expenses"
                                    element={
                                        <Suspense
                                            fallback={<div>Ładowanie...</div>}>
                                            <Expenses />
                                        </Suspense>
                                    }
                                />
                                <Route
                                    path="/income"
                                    element={
                                        <Suspense
                                            fallback={<div>Ładowanie...</div>}>
                                            <Income />
                                        </Suspense>
                                    }
                                />
                                <Route
                                    path="/settings"
                                    element={
                                        <Suspense
                                            fallback={<div>Ładowanie...</div>}>
                                            <Settings />
                                        </Suspense>
                                    }
                                />
                            </Routes>
                        </Layout>
                    </BrowserRouter>
                </GlobalProvider>
            </QueryClientProvider>
        </ThemeProvider>
    );
}

export default App;

