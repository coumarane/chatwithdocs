import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_BACKEND_API!

export const registerUser = async (userData: { username: string; email: string; password: string, hasAgreedTerms: boolean }) => {
    const response = await axios.post(`${API_URL}/api/register`, userData);
  return response.data;
};
