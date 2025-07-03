import React from 'react';

interface ProfileHeaderProps {
  avatarUrl: string;
  name: string;
  title: string;
  location: string;
  socialLinks: { platform: string; url: string }[];
}

const ProfileHeader: React.FC<ProfileHeaderProps> = ({ avatarUrl, name, title, location, socialLinks }) => {
  return (
    <div className="flex flex-col md:flex-row items-center md:items-end gap-4 md:gap-8 p-4 bg-gradient-to-r from-blue-100 to-blue-50 rounded-lg shadow">
      <img
        src={avatarUrl}
        alt="User Avatar"
        className="w-24 h-24 rounded-full border-4 border-white shadow-md object-cover"
      />
      <div className="flex-1 text-center md:text-left">
        <h2 className="text-2xl font-bold">{name}</h2>
        <div className="text-gray-600">{title}</div>
        <div className="text-gray-500 text-sm">{location}</div>
        <div className="flex justify-center md:justify-start gap-3 mt-2">
          {socialLinks.map((link) => (
            <a key={link.platform} href={link.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
              {link.platform}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProfileHeader;
