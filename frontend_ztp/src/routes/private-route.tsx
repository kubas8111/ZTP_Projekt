import { Outlet, Navigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";

export default function PrivateRoute() {
    const { userUsername } = useAuth();
    return userUsername ? <Outlet /> : <Navigate to="/login" replace />;
}
