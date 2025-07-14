import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authApi } from './api';

const Login: React.FC = () => {
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
    setSuccess('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.email || !form.password) {
      setError('All fields are required.');
      return;
    }
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const data = await authApi.login({ email: form.email, password: form.password });
      if (data && data.token) {
        localStorage.setItem('token', data.token);
        setSuccess('Login successful!');
        navigate('/profile');
      } else {
        setError(data.message || 'Login failed');
      }
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-2">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-bold text-center mb-6">Login</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block font-medium">
            Username or Email
            <input
              type="text"
              name="email"
              placeholder="Username or Email"
              value={form.email}
              onChange={handleChange}
              className="w-full p-2 border rounded mt-1"
            />
            {error && !form.email && (
              <div className="text-red-500 text-sm">
                Username or Email is required.
              </div>
            )}
          </label>
          <label className="block font-medium">
            Password
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              className="w-full p-2 border rounded mt-1"
            />
            {error && !form.password && (
              <div className="text-red-500 text-sm">Password is required.</div>
            )}
          </label>
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
          {error && form.email && form.password && (
            <div className="text-red-500 text-center text-sm mt-2">{error}</div>
          )}
          {success && (
            <div className="text-green-600 text-center text-sm mt-2">{success}</div>
          )}
        </form>
        <p className="mt-4 text-center text-sm">
          Don't have an account?{' '}
          <Link to="/signup" className="text-blue-600 hover:underline">
            Signup
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;