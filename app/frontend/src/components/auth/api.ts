const API_URL = 'http://localhost:5000';

export const authApi = {
  login: async (credentials: { email: string; password: string }) => {
    const response = await fetch(`${API_URL}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: credentials.email, password: credentials.password }),
    });
    return response.json();
  },

  signup: async (userData: { email: string; password: string; name: string }) => {
    const response = await fetch(`${API_URL}/api/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: userData.email, password: userData.password, username: userData.name }),
    });
    return response.json();
  },
}; 