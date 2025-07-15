import React, { useEffect, useRef } from "react";

interface SettingsDialogProps {
  open: boolean;
  onClose: () => void;
  darkMode: boolean;
  onToggleDark: () => void;
  onLogout: () => void;
}

const SettingsDialog: React.FC<SettingsDialogProps> = ({ open, onClose, darkMode, onToggleDark, onLogout }) => {
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dialogRef.current && !dialogRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (open) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [open, onClose]);

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 dark:bg-black/60 transition-colors">
      <div ref={dialogRef} className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 w-full max-w-xs transition-colors duration-300 relative">
        <button
          className="absolute top-2 right-2 text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 text-xl"
          onClick={onClose}
          aria-label="Close settings"
        >
          ×
        </button>
        <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Settings</h2>
        <div className="flex items-center justify-between mb-4">
          <span className="text-gray-700 dark:text-gray-200">Dark Mode</span>
          <button
            className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors duration-200 ${darkMode ? 'bg-primary' : 'bg-gray-300'}`}
            onClick={onToggleDark}
            aria-label="Toggle dark mode"
          >
            <span
              className={`bg-white w-4 h-4 rounded-full shadow transform transition-transform duration-200 ${darkMode ? 'translate-x-6' : ''}`}
            />
          </button>
        </div>
        <button
          className="w-full btn btn-secondary mt-2"
          onClick={onLogout}
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default SettingsDialog;
