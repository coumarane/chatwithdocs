import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_BACKEND_API! || "http://127.0.0.1:8000"

export const registerUser = async (userData: { username: string; email: string; password: string, hasAgreedTerms: boolean }) => {
    const response = await axios.post(`${API_URL}/api/register`, userData);
    return response.data;
};

export const resendVerificationEmail = async (email: string) => {
    const response = await axios.post(`${API_URL}/api/resend-verification`, { email });
    return response.data;
};

export const verifyEmailCode = async (data: { email: string; code: string }) => {
    const response = await axios.post(`${API_URL}/api/verify-code`, data);
    return response.data;
};