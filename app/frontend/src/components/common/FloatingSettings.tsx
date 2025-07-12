import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import SettingsDialog from "./SettingsDialog";

const FloatingSettings: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark' ||
      (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('profile_cache');
    navigate('/login');
  };

  return (
    <>
      <button
        className="fixed z-50 bottom-6 right-6 bg-card-light dark:bg-card-dark shadow-lg rounded-full p-4 text-2xl text-gray-500 hover:text-primary dark:hover:text-primary transition-colors duration-300 border border-gray-200 dark:border-gray-700"
        onClick={() => setOpen(true)}
        aria-label="Open settings"
      >
        <span role="img" aria-label="settings">⚙️</span>
      </button>
      <SettingsDialog
        open={open}
        onClose={() => setOpen(false)}
        darkMode={darkMode}
        onToggleDark={() => setDarkMode((d) => !d)}
        onLogout={handleLogout}
      />
    </>
  );
};

export default FloatingSettings;
