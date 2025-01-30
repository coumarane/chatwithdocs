"use client";

import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Menu, X } from "lucide-react";

const Navbar = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <nav className="w-full bg-white shadow-md fixed top-0 z-50">
            <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                {/* Logo */}
                <Link href="/" className="text-2xl font-bold text-gray-900">
                    ChatWith<span className="text-blue-600">Docs</span>
                </Link>

                {/* Desktop Menu */}
                <div className="hidden md:flex space-x-6">
                    <Link href="/about" className="hover:text-blue-600">About</Link>
                    <Link href="/features" className="hover:text-blue-600">Features</Link>
                    <Link href="/pricing" className="hover:text-blue-600">Pricing</Link>
                    <Link href="/faq" className="hover:text-blue-600">FAQ</Link>
                    <Link href="/docs" className="hover:text-blue-600">Docs</Link>
                    <Link href="/blog" className="hover:text-blue-600">Blog</Link>
                </div>

                {/* Auth Buttons */}
                <div className="hidden md:flex items-center space-x-4">
                    <Link href="/auth/login">
                        <Button variant="outline">Login</Button>
                    </Link>
                    <Link href="/auth/register">
                        <Button>Sign Up</Button>
                    </Link>
                </div>

                {/* Mobile Menu Toggle */}
                <button onClick={() => setIsOpen(!isOpen)} className="md:hidden">
                    {isOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <div className="md:hidden bg-white shadow-md absolute w-full left-0 top-16 p-4 flex flex-col space-y-4">
                    <Link href="/about" onClick={() => setIsOpen(false)}>About</Link>
                    <Link href="/features" onClick={() => setIsOpen(false)}>Features</Link>
                    <Link href="/pricing" onClick={() => setIsOpen(false)}>Pricing</Link>
                    <Link href="/faq" onClick={() => setIsOpen(false)}>FAQ</Link>
                    <Link href="/docs" onClick={() => setIsOpen(false)}>Docs</Link>
                    <Link href="/blog" onClick={() => setIsOpen(false)}>Blog</Link>
                    <Link href="/auth/login" onClick={() => setIsOpen(false)}>
                        <Button variant="outline" className="w-full">Login</Button>
                    </Link>
                    <Link href="/auth/register" onClick={() => setIsOpen(false)}>
                        <Button className="w-full">Get Started</Button>
                    </Link>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
