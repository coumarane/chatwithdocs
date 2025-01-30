import React from 'react';
import type { Metadata, Viewport } from 'next';
import './globals.css';
import { Manrope } from 'next/font/google';
import { ReactQueryProvider } from '../components/site/ReactQueryProvider';
import { cn } from "@/lib/utils"
import { fontHeading, fontInter, fontUrbanist } from "../config/fonts"
import { siteConfig } from "../config/site"
import { Toaster } from '@/components/ui/toaster';
import Navbar from '@/components/site/Navbar';
import Footer from '@/components/site/Footer';

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

export const metadata: Metadata = {
    metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL!),
    title: {
        default: siteConfig.name,
        template: `%s - ${siteConfig.name}`,
    },
    description: siteConfig.description,
    authors: [
        {
            name: siteConfig.author,
            url: siteConfig.links.authorsWebsite,
        },
    ],
    creator: siteConfig.author,
    keywords: siteConfig.keywords,
    robots: {
        index: true,
        follow: true,
    },

    openGraph: {
        type: "website",
        locale: "fr_FR",
        url: siteConfig.url,
        title: siteConfig.name,
        description: siteConfig.description,
        siteName: siteConfig.name,
    },
    twitter: {
        card: "summary_large_image",
        title: siteConfig.name,
        description: siteConfig.description,
        creator: siteConfig.author,
    },
    icons: {
        icon: "/favicon.ico",
    },
}


const manrope = Manrope({ subsets: ['latin'] });

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en"
            className={`bg-white dark:bg-gray-950 text-black dark:text-white ${manrope.className}`}
        >
            <body
                className={cn(
                    "w-full bg-background bg-gradient-to-r from-background to-pink-400/10 font-sans antialiased",
                    fontInter.variable,
                    fontUrbanist.variable,
                    fontHeading.variable
                )}
            >
                <ReactQueryProvider>
                    <Navbar />
                    {children}
                    <Footer />
                    <Toaster />
                </ReactQueryProvider>
            </body>
        </html>
    );
}
