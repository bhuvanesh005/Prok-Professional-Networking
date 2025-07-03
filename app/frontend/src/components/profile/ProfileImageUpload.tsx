import React, { useRef } from 'react';

interface ProfileImageUploadProps {
  imageUrl: string | null;
  onImageChange: (file: File | null) => void;
  uploading: boolean;
  progress: number;
}

const ProfileImageUpload: React.FC<ProfileImageUploadProps> = ({ imageUrl, onImageChange, uploading, progress }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onImageChange(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onImageChange(e.target.files[0]);
    }
  };

  return (
    <div
      className="flex flex-col items-center mb-4"
      onDrop={handleDrop}
      onDragOver={e => e.preventDefault()}
    >
      <div
        className="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden mb-2 cursor-pointer border-2 border-dashed border-gray-400 hover:border-blue-500"
        onClick={() => fileInputRef.current?.click()}
      >
        {imageUrl ? (
          <img src={imageUrl} alt="Avatar Preview" className="object-cover w-full h-full" />
        ) : (
          <span className="text-gray-500">Upload</span>
        )}
      </div>
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        className="hidden"
        onChange={handleFileChange}
      />
      {uploading && (
        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
          <div
            className="bg-blue-500 h-2 rounded-full"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      )}
    </div>
  );
};

export default ProfileImageUpload;
