import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogDescription,
} from "@/components/ui/dialog";

import { fetchGetMe, fetchPutMe, fetchDeleteMe } from "@/api/apiService";
import { useAuth } from "@/context/AuthContext";
import { User } from "@/types";
import { toast } from "sonner";

const Settings = () => {
    const { logout } = useAuth();
    const queryClient = useQueryClient();
    const [isEditing, setIsEditing] = useState(false);
    const [email, setEmail] = useState("");
    const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
    const [password, setPassword] = useState("");

    const {
        data: user,
        isLoading: userLoading,
        isError: userError,
    } = useQuery<User>({
        queryKey: ["me"],
        queryFn: fetchGetMe,
        staleTime: 1000 * 60 * 5,
        retry: false,
        enabled: !!localStorage.getItem("username"),
    });

    useEffect(() => {
        if (user) {
            setEmail(user.email);
        }
    }, [user]);

    const mutation = useMutation({
        mutationFn: fetchPutMe,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["me"] });
            setIsEditing(false);
        },
    });

    const deleteMutation = useMutation({
        mutationFn: () => fetchDeleteMe(password),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["me"] });
            logout();
        },
    });

    const handleSave = () => {
        if (!email) {
            toast.error("Email jest wymagany");
            return;
        }
        mutation.mutate({ email });
    };

    const handleDelete = () => {
        deleteMutation.mutate();
    };

    if (!user) return <p>Brak danych użytkownika</p>;
    if (userLoading) {
        return <p>Ładowanie danych użytkownika…</p>;
    }
    if (userError || !user) {
        return <p>Nie udało się pobrać danych.</p>;
    }

    console.log(user);

    return (
        <div className="max-w-md mx-auto mt-10 text-center">
            {/* Avatar */}
            <div className="flex justify-center mb-4">
                <img
                    src={user.avatar || "https://github.com/shadcn.png"}
                    alt="Avatar"
                    className="w-24 h-24 rounded-full object-cover border shadow"
                />
            </div>

            {/* Username */}
            <h2 className="text-xl font-semibold">{user.username}</h2>

            {/* Email */}
            <div className="mt-6">
                <label
                    htmlFor="email"
                    className="block text-sm text-gray-600 mb-1">
                    Adres e-mail
                </label>
                <div className="flex items-center gap-2 justify-center">
                    <Input
                        id="email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        disabled={!isEditing}
                        className="max-w-xs"
                    />
                    {!isEditing ? (
                        <Button
                            size="icon"
                            variant="outline"
                            onClick={() => setIsEditing(true)}>
                            <Pencil size={16} />
                        </Button>
                    ) : (
                        <Button
                            onClick={handleSave}
                            disabled={mutation.isPending}>
                            Zapisz
                        </Button>
                    )}
                </div>
            </div>

            {/* Delete account */}
            <div className="mt-10 border-t pt-6">
                <Button
                    variant="destructive"
                    onClick={() => setConfirmDialogOpen(true)}>
                    <Trash2 className="mr-2 h-4 w-4" />
                    Usuń konto
                </Button>
            </div>

            {/* Confirm deletion dialog */}
            <Dialog
                open={confirmDialogOpen}
                onOpenChange={setConfirmDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Potwierdź usunięcie konta</DialogTitle>
                        <DialogDescription>
                            Tej operacji nie można cofnąć. Aby kontynuować,
                            wpisz swoje hasło:
                        </DialogDescription>
                    </DialogHeader>

                    <Input
                        type="password"
                        placeholder="Wpisz hasło"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="mt-2"
                    />

                    <DialogFooter className="mt-4 flex justify-between">
                        <Button
                            variant="outline"
                            onClick={() => setConfirmDialogOpen(false)}>
                            Anuluj
                        </Button>
                        <Button
                            variant="destructive"
                            onClick={handleDelete}
                            disabled={!password || deleteMutation.isPending}>
                            Potwierdź usunięcie
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default Settings;
