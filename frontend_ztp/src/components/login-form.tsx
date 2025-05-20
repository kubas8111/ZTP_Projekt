import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/context/AuthContext";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { showError } from "@/lib/toast-maker";
import { useQueryClient } from "@tanstack/react-query";

export function LoginForm({
    className,
    ...props
}: React.ComponentProps<"div">) {
    const { login } = useAuth();
    const navigate = useNavigate();

    const [form, setForm] = useState({ username: "", password: "" });

    const queryClient = useQueryClient();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) =>
        setForm({ ...form, [e.target.id]: e.target.value });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            await login(form.username, form.password);
            await queryClient.invalidateQueries({ queryKey: ["me"] });
            navigate("/");
        } catch (err: any) {
            if (import.meta.env.DEV) {
                // console.log(JSON.stringify(form, null, 2));
                console.log(err);
            }
            showError(err);
        }
    };

    return (
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Card>
                <CardHeader>
                    <CardTitle>Login to your account</CardTitle>
                    <CardDescription>
                        Enter your credentials below to log in
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form>
                        <div className="flex flex-col gap-6">
                            <div className="grid gap-3">
                                <Label htmlFor="username">Username</Label>
                                <Input
                                    id="username"
                                    type="text"
                                    placeholder="johndoe"
                                    required
                                    value={form.username}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="grid gap-3">
                                <div className="flex items-center">
                                    <Label htmlFor="password">Password</Label>
                                    {/* <a
                                        href="#"
                                        className="ml-auto inline-block text-sm underline-offset-4 hover:underline">
                                        Forgot your password?
                                    </a> */}
                                </div>
                                <Input
                                    id="password"
                                    type="password"
                                    required
                                    value={form.password}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="flex flex-col gap-3">
                                <Button
                                    type="button"
                                    onClick={(e) => handleSubmit(e)}
                                    className="w-full">
                                    Login
                                </Button>
                            </div>
                        </div>
                        <div className="mt-4 text-center text-sm">
                            Don&apos;t have an account?{" "}
                            <Link
                                to="/register"
                                className="underline underline-offset-4">
                                Sign up
                            </Link>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
