const API_URL = 'http://localhost:5000';

export const profileApi = {
  getProfile: async () => {
    const token = localStorage.getItem('token');
    console.log('[DEBUG] Using JWT token:', token);
    const response = await fetch(`${API_URL}/api/profile`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    const data = await response.json();
    console.log('[DEBUG] /api/profile response:', data);
    return data;
  },

  updateProfile: async (profileData: any) => {
    const token = localStorage.getItem('token');
    console.log('[DEBUG] Using JWT token:', token);
    const response = await fetch(`${API_URL}/api/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(profileData),
    });
    const data = await response.json();
    console.log('[DEBUG] /api/profile PUT response:', data);
    return data;
  },
};