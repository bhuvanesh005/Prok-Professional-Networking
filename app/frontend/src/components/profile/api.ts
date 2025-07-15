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

  uploadProfileImage: async (file: File) => {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('image', file);
    const response = await fetch(`${API_URL}/api/profile/image`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });
    const data = await response.json();
    return data;
  },

  // Test method that bypasses authentication
  getProfileTest: async () => {
    console.log('[DEBUG] Using test endpoint (no auth required)');
    const response = await fetch(`${API_URL}/api/profile/test`);
    const data = await response.json();
    console.log('[DEBUG] /api/profile/test response:', data);
    return data;
  },
};