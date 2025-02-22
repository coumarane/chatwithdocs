import React from 'react';
import type { Viewport } from 'next';
import '../globals.css';
import { Manrope } from 'next/font/google';

export const viewport: Viewport = {
    width: "device-width",
    initialScale: 1,
    minimumScale: 1,
    maximumScale: 1,
    themeColor: [
        { media: "(prefers-color-scheme: light)", color: "white" },
        { media: "(prefers-color-scheme: dark)", color: "black" },
    ],
}


const manrope = Manrope({ subsets: ['latin'] });

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en"
            className={`bg-white dark:bg-gray-950 text-black dark:text-white ${manrope.className}`}
        >
            <body>
                {children}
            </body>
        </html>
    );
}
