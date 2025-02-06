import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function VerifyEmailPage() {
    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-50">
            <div className="w-full max-w-md bg-white shadow-lg rounded-lg p-6 text-center">
                <h2 className="text-2xl font-semibold text-gray-900">Verify Your Email</h2>
                <p className="text-gray-500 mt-2">
                    We have sent a verification link to your email. Please check your inbox and click on the link to activate your account.
                </p>

                <div className="mt-6">
                    <p className="text-gray-500 text-sm">
                        Didn’t receive the email? <Link href="/auth/resend-verification" className="text-blue-600 hover:underline">Resend verification</Link>
                    </p>
                </div>

                <Button className="mt-6 w-full" asChild>
                    <Link href="/">Go to Home</Link>
                </Button>
            </div>
        </div>
    );
}
