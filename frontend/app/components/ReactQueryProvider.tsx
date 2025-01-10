'use client'; // Mark as a Client Component

import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

type ReactQueryProviderProps = {
    children: React.ReactNode;
};

const queryClient = new QueryClient();

export const ReactQueryProvider: React.FC<ReactQueryProviderProps> = ({ children }) => {
    return (
        <QueryClientProvider client={queryClient}>
            {children}
        </QueryClientProvider>
    );
};
