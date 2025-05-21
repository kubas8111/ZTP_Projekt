import { Link, useLocation, useNavigate } from "react-router-dom";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar";
import {
    Home,
    TrendingDown,
    TrendingUp,
    DollarSign,
    Settings,
    ChevronUp,
    ChartNoAxesCombined,
} from "lucide-react";
import { useAuth } from "@/context/AuthContext";

const menuItems = [
    { title: "Dashboard", path: "/", icon: Home },
    { title: "Wydatki", path: "/expenses", icon: TrendingDown },
    { title: "Przychody", path: "/income", icon: TrendingUp },
    { title: "Podsumowanie", path: "/summary", icon: DollarSign },
    { title: "Wykresy", path: "/charts", icon: ChartNoAxesCombined },
    { title: "Ustawienia", path: "/settings", icon: Settings },
];

export default function AppSidebar() {
    const location = useLocation();
    const navigate = useNavigate();
    const { userUsername, logout } = useAuth();

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    /** dwie pierwsze litery nazwy użytkownika do fallbacku */
    const initials = (userUsername ?? "GN").slice(0, 2).toUpperCase();

    return (
        <div className="flex h-screen">
            <Sidebar className="w-64 border-r">
                <SidebarContent>
                    <SidebarGroup>
                        <SidebarGroupLabel>Nawigacja</SidebarGroupLabel>
                        <SidebarGroupContent>
                            <SidebarMenu>
                                {menuItems.map((item) => (
                                    <SidebarMenuItem key={item.path}>
                                        <SidebarMenuButton asChild>
                                            <Link
                                                to={item.path}
                                                className={`flex items-center gap-3 px-4 py-2 text-sm font-medium rounded-md transition ${
                                                    location.pathname ===
                                                    item.path
                                                        ? "bg-muted"
                                                        : "hover:bg-accent"
                                                }`}>
                                                <item.icon className="h-4 w-4" />
                                                <span>{item.title}</span>
                                            </Link>
                                        </SidebarMenuButton>
                                    </SidebarMenuItem>
                                ))}
                            </SidebarMenu>
                        </SidebarGroupContent>
                    </SidebarGroup>
                </SidebarContent>
                <SidebarFooter className="border-t">
                    <SidebarMenu>
                        <SidebarMenuItem>
                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <SidebarMenuButton className="w-full flex items-center gap-3 px-4 py-2 text-sm font-medium rounded-md hover:bg-accent">
                                        <Avatar className="h-6 w-6">
                                            {/* Tutaj możesz podmienić src na realny link z backendu */}
                                            <AvatarImage src="https://github.com/shadcn.png" />
                                            <AvatarFallback>
                                                {initials}
                                            </AvatarFallback>
                                        </Avatar>
                                        <span>{userUsername ?? "Guest"}</span>
                                        <ChevronUp className="ml-auto h-4 w-4" />
                                    </SidebarMenuButton>
                                </DropdownMenuTrigger>

                                <DropdownMenuContent
                                    side="top"
                                    className="w-[--radix-popper-anchor-width]">
                                    {userUsername ? (
                                        <>
                                            <DropdownMenuItem asChild>
                                                <Link to="/settings">
                                                    <span>Account</span>
                                                </Link>
                                            </DropdownMenuItem>
                                            <DropdownMenuItem
                                                onClick={handleLogout}>
                                                <span>Sign out</span>
                                            </DropdownMenuItem>
                                        </>
                                    ) : (
                                        <DropdownMenuItem asChild>
                                            <Link to="/login">
                                                <span>Sign in</span>
                                            </Link>
                                        </DropdownMenuItem>
                                    )}
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </SidebarMenuItem>
                    </SidebarMenu>
                </SidebarFooter>
            </Sidebar>
        </div>
    );
}
