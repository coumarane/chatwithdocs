'use client'; // Mark as a Client Component

import React from 'react';
import { usePosts } from './hooks/usePost';

export default function Home() {
    const { data, isLoading, error } = usePosts(20); // Fetch 20 posts

    if (isLoading) return <div>Loading...</div>;
    if (error instanceof Error) return <div>Error: {error.message}</div>;

    return (
        <div style={{ padding: '20px' }}>
            <h1>Posts</h1>
            <ul>
                {data?.map((post) => (
                    <li key={post.id}>
                        <h2>{post.title}</h2>
                        <p>{post.body}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}
