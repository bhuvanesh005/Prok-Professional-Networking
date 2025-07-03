import React from 'react';

interface ProfileFormInputProps {
  label: string;
  name: string;
  type?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
  error?: string;
  textarea?: boolean;
  placeholder?: string;
}

const ProfileFormInput: React.FC<ProfileFormInputProps> = ({
  label,
  name,
  type = 'text',
  value,
  onChange,
  error,
  textarea = false,
  placeholder = '',
}) => (
  <div className="mb-4">
    <label className="block font-medium mb-1" htmlFor={name}>{label}</label>
    {textarea ? (
      <textarea
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full p-2 border rounded"
        rows={4}
      />
    ) : (
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full p-2 border rounded"
      />
    )}
    {error && <div className="text-red-500 text-sm mt-1">{error}</div>}
  </div>
);

export default ProfileFormInput;
