"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { resendVerificationEmail } from "@/lib/api/auth";


export default function ResendVerificationPage() {
    const [email, setEmail] = useState("");
    const { toast } = useToast();

    const mutation = useMutation({
        mutationFn: resendVerificationEmail,
        onSuccess: () => {
            toast({ title: "✅ Email Sent", description: "Check your inbox for the verification link." });
        },
        onError: () => {
            toast({ title: "❌ Failed to Send", description: "Please try again later.", variant: "destructive" });
        },
    });

    const handleResend = () => mutation.mutate(email);

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-50">
            <div className="w-full max-w-md bg-white shadow-lg rounded-lg p-6 text-center">
                <h2 className="text-2xl font-semibold text-gray-900">Resend Verification Email</h2>
                <p className="text-gray-500 mt-2">Enter your email address to receive a new verification link.</p>

                <div className="mt-4">
                    <Input type="email" placeholder="Enter your email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>

                <Button onClick={handleResend} className="mt-4 w-full" disabled={mutation.isPending}>
                    {mutation.isPending ? "Sending..." : "Resend Email"}
                </Button>
            </div>
        </div>
    );
}
