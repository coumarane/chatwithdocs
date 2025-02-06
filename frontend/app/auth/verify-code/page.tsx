"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { verifyEmailCode } from "@/lib/api/auth";
import axios from "axios";


export default function VerifyCodePage() {
    const [email, setEmail] = useState("");
    const [code, setCode] = useState("");
    const { toast } = useToast();
    const router = useRouter();

    const mutation = useMutation({
        mutationFn: verifyEmailCode,
        onSuccess: () => {
            toast({ title: "✅ Verification Successful", description: "Redirecting to your dashboard..." });

            setTimeout(() => {
                router.push("/dashboard"); // ✅ Redirect after successful verification
            }, 2000);
        },
        onError: (error: unknown) => {
            let errorMessage = "An error occurred. Please try again.";

            if (axios.isAxiosError(error) && error.response) {
                errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage;
            }

            toast({
                title: "❌ Verification Failed",
                description: errorMessage,
                variant: "destructive",
            });
        },
    });

    const handleVerify = () => {
        mutation.mutate({ email, code });
    };

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-50">
            <div className="w-full max-w-md bg-white shadow-lg rounded-lg p-6 text-center">
                <h2 className="text-2xl font-semibold text-gray-900">Verify Your Email</h2>
                <p className="text-gray-500 mt-2">
                    Enter the verification code sent to your email.
                </p>

                <div className="mt-4">
                    <Input
                        type="email"
                        placeholder="Enter your email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                <div className="mt-4">
                    <Input
                        type="text"
                        placeholder="Enter verification code"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                    />
                </div>

                <Button onClick={handleVerify} className="mt-4 w-full" disabled={mutation.isPending}>
                    {mutation.isPending ? "Verifying..." : "Verify Code"}
                </Button>
            </div>
        </div>
    );
}
