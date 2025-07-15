import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../navigation/Navbar';
import FloatingSettings from '../common/FloatingSettings';

const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <main className="pt-16">
        <Outlet />
      </main>
      <FloatingSettings />
    </div>
  );
};

export default Layout; 