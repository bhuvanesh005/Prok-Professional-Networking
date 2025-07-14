import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authApi } from './api';

const Signup: React.FC = () => {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: '',
  });
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
    if (!form.username || !form.email || !form.password || !form.confirm_password) {
      setError('All fields are required.');
      return;
    }
    if (form.password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    if (form.password !== form.confirm_password) {
      setError('Passwords do not match.');
      return;
    }
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const data = await authApi.signup({
        name: form.username,
        email: form.email,
        password: form.password,
      });
      if (data && data.message === 'User created successfully') {
        setSuccess('Signup successful! You can now log in.');
        setForm({ username: '', email: '', password: '', confirm_password: '' });
        navigate('/login');
      } else {
        setError(data.message || 'Signup failed');
      }
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-2">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-bold text-center mb-6">Sign Up</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block font-medium">Username
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={form.username}
              onChange={handleChange}
              className="w-full p-2 border rounded mt-1"
            />
            {error && !form.username && <div className="text-red-500 text-sm">Username is required.</div>}
          </label>
          <label className="block font-medium">Email
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={form.email}
              onChange={handleChange}
              className="w-full p-2 border rounded mt-1"
            />
            {error && !form.email && <div className="text-red-500 text-sm">Email is required.</div>}
          </label>
          <label className="block font-medium">Password
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              className="w-full p-2 border rounded mt-1"
            />
            {error && form.password.length < 8 && <div className="text-red-500 text-sm">Password must be at least 8 characters.</div>}
          </label>
          <label className="block font-medium">Confirm Password
            <input
              type="password"
              name="confirm_password"
              placeholder="Confirm Password"
              value={form.confirm_password}
              onChange={handleChange}
              className="w-full p-2 border rounded mt-1"
            />
            {error && form.password !== form.confirm_password && <div className="text-red-500 text-sm">Please confirm your password.</div>}
          </label>
          <button type="submit" className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700" disabled={loading}>
            {loading ? 'Signing up...' : 'Signup'}
          </button>
          {error && form.username && form.email && form.password && form.confirm_password && (
            <div className="text-red-500 text-center text-sm mt-2">{error}</div>
          )}
          {success && (
            <div className="text-green-600 text-center text-sm mt-2">{success}</div>
          )}
        </form>
        <p className="mt-4 text-center text-sm">
          Already have an account?{' '}
          <Link to="/login" className="text-blue-600 hover:underline">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;