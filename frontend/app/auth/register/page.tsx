"use client";

import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { FaGoogle, FaGithub } from "react-icons/fa";
import { useMutation } from "@tanstack/react-query";
import { registerUser } from "@/lib/api/auth";
import { useToast } from "@/hooks/use-toast"
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import axios from "axios";

// Define the type for form data
type RegisterFormData = {
    username: string;
    email: string;
    password: string;
    hasAgreedTerms: boolean;
};

// Define validation schema
const schema = z.object({
    username: z.string().min(3, "Username must be at least 3 characters"),
    email: z.string().email("Invalid email format"),
    password: z.string().min(6, "Password must be at least 6 characters"),
    hasAgreedTerms: z.boolean().refine((val) => val === true, {
        message: "You must agree to the terms",
    }),
});

export default function RegisterPage() {

    const { register, handleSubmit, formState: { errors }, setValue, clearErrors } = useForm<RegisterFormData>({
        resolver: zodResolver(schema),
    });

    // const [username, setUsername] = useState("");
    // const [email, setEmail] = useState("");
    // const [password, setPassword] = useState("");
    // const [isChecked, setIsChecked] = useState(false);

    const { toast } = useToast();
    const router = useRouter();

    // Handle checkbox manually to ensure boolean
    const handleCheckboxChange = (checked: boolean) => {
        setValue("hasAgreedTerms", checked);
        if (checked) clearErrors("hasAgreedTerms");
    };

    // Mutation for signup
    const mutation = useMutation({
        mutationFn: (formData: RegisterFormData) => registerUser(formData),
        onSuccess: () => {
            toast({
                title: "🎉 Registration Successful!",
                description: "Redirecting to your dashboard...",
            });

            setTimeout(() => {
                router.push("/auth/verify-email"); // Redirect to verify-email
            }, 2000); // Add delay for smooth user experience
        },
        onError: (error: unknown) => {
            let errorMessage = "An error occurred. Please try again.";

            if (axios.isAxiosError(error) && error.response) {
                errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage;
            }

            toast({
                title: "❌ Signup Failed",
                description: errorMessage,
                variant: "destructive",
            });
        },
    });

    const onSubmit = (data: RegisterFormData) => mutation.mutate(data);

    // const handleRegister = (e: React.FormEvent) => {
    //     e.preventDefault();
    //     if (!isChecked) return alert("Please agree to the terms and privacy policy.");
    //     if (username.trim() === '') return alert("Username is required");
    //     mutation.mutate({ username, email, password, has_agreed_terms: isChecked });
    // };

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-50">
            <div className="w-full max-w-md bg-white shadow-lg rounded-lg p-6">
                <h2 className="text-2xl font-semibold text-gray-900 text-center">Create Your Account</h2>
                <p className="text-gray-500 text-center text-sm mt-2">
                    Already have an account?{" "}
                    <Link href="/auth/login" className="text-blue-600 hover:underline">Sign in</Link>
                </p>

                {/* Social Auth Buttons */}
                <div className="mt-6 space-y-3">
                    <Button variant="outline" className="w-full flex items-center gap-2">
                        <FaGoogle size={18} className="text-red-500" />
                        Sign up with Google
                    </Button>
                    <Button variant="outline" className="w-full flex items-center gap-2">
                        <FaGithub size={18} />
                        Sign up with GitHub
                    </Button>
                </div>

                {/* Divider */}
                <div className="relative my-6">
                    <div className="absolute inset-0 flex items-center">
                        <span className="w-full border-t border-gray-300"></span>
                    </div>
                    <div className="relative flex justify-center text-sm">
                        <span className="bg-white px-2 text-gray-500">Or continue with email</span>
                    </div>
                </div>

                {/* Signup Form */}
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <div>
                        <label className="text-sm font-medium text-gray-700">Username</label>
                        <Input type="text" placeholder="Enter a username" {...register("username")} />
                        {errors.username?.message && <p className="text-red-500 text-xs mt-1">{String(errors.username.message)}</p>}
                    </div>

                    <div>
                        <label className="text-sm font-medium text-gray-700">Email</label>
                        <Input type="email" placeholder="Enter your email" {...register("email")} />
                        {errors.email?.message && <p className="text-red-500 text-xs mt-1">{String(errors.email.message)}</p>}
                    </div>

                    <div>
                        <label className="text-sm font-medium text-gray-700">Password</label>
                        <Input type="password" placeholder="Enter your password" {...register("password")} />
                        {errors.password?.message && <p className="text-red-500 text-xs mt-1">{String(errors.password.message)}</p>}
                    </div>

                    {/* Terms and Privacy Checkbox */}
                    <div className="flex items-start space-x-2">
                        <Checkbox
                            id="terms"
                            onCheckedChange={handleCheckboxChange}
                            {...register("hasAgreedTerms")} />
                        <label htmlFor="terms" className="text-sm text-gray-600">
                            I agree to the{" "}
                            <Link href="/terms" className="text-blue-600 hover:underline">Terms</Link> and{" "}
                            <Link href="/privacy" className="text-blue-600 hover:underline">Privacy Policy</Link>.
                        </label>
                    </div>
                    {errors.hasAgreedTerms?.message && <p className="text-red-500 text-xs mt-1">{String(errors.hasAgreedTerms.message)}</p>}

                    <Button type="submit" className="w-full" disabled={mutation.isPending}>
                        {mutation.isPending ? "Creating account..." : "Create Account"}
                    </Button>
                </form>
            </div>
        </div>
    );
}
