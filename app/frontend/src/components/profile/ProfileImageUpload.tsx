import React, { useRef } from 'react';

interface ProfileImageUploadProps {
  imageUrl: string | null;
  onImageChange: (file: File | null, error?: string) => void;
  uploading: boolean;
  progress: number;
}

const MAX_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png'];

const ProfileImageUpload: React.FC<ProfileImageUploadProps> = ({ imageUrl, onImageChange, uploading, progress }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [error, setError] = React.useState<string | null>(null);

  const validateFile = (file: File) => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      
      onImageChange(null, 'Only JPG and PNG images are allowed.');
      return false;
    }
    if (file.size > MAX_SIZE) {
      setError('Image must be less than 5MB.');
      onImageChange(null, 'Image must be less than 5MB.');
      return false;
    }
    setError(null);
    return true;
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (validateFile(file)) {
        onImageChange(file);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (validateFile(file)) {
        onImageChange(file);
      }
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
        accept="image/jpeg,image/png"
        ref={fileInputRef}
        className="hidden"
        onChange={handleFileChange}
      />
      {error && <div className="text-red-500 text-xs mt-1">{error}</div>}
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
