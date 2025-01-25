'use client'; // Mark as a Client Component

import React from 'react';
import { usePosts } from '../../../hooks/usePost';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

export default function Posts() {
    const { data, isLoading, error } = usePosts(20); // Fetch 20 posts

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h1 className="text-2xl font-bold mb-4">Posts</h1>

            {isLoading && (
                <div className="space-y-4">
                    {Array.from({ length: 5 }).map((_, idx) => (
                        <Skeleton key={idx} className="h-16 w-full" />
                    ))}
                </div>
            )}

            {error instanceof Error && (
                <Alert variant="destructive" className="my-4">
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>{error.message}</AlertDescription>
                </Alert>
            )}

            {data && (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {data.map((post) => (
                        <Card key={post.id}>
                            <CardHeader>
                                <CardTitle className="text-lg font-semibold">{post.title}</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p>{post.body}</p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
