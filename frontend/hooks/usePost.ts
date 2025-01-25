import { useQuery } from '@tanstack/react-query';

export type Post = {
  id: number;
  title: string;
  body: string;
};

// Fetch posts from FastAPI backend
const fetchPosts = async (limit: number): Promise<Post[]> => {
  const response = await fetch('http://127.0.0.1:8000/api/posts');
  if (!response.ok) {
    throw new Error('Failed to fetch posts');
  }
  const data: Post[] = await response.json();
  return data.slice(0, limit); // Limit the posts to the specified number
};

export const usePosts = (limit: number) => {
  return useQuery<Post[]>({
    queryKey: ['posts', limit],
    queryFn: () => fetchPosts(limit),
  });
};
