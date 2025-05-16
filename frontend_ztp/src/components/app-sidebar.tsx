import { Link, useLocation } from "react-router-dom";
import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Home, TrendingDown, TrendingUp, Settings } from "lucide-react";

const menuItems = [
    { title: "Dashboard", path: "/", icon: Home },
    { title: "Wydatki", path: "/expenses", icon: TrendingDown },
    { title: "Przychody", path: "/income", icon: TrendingUp },
    { title: "Ustawienia", path: "/settings", icon: Settings },
];

export default function AppSidebar() {
    const location = useLocation();

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
            </Sidebar>
        </div>
    );
}

