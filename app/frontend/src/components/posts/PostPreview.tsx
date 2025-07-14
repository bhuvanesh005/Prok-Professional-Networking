import React from 'react';

interface PostPreviewProps {
  title: string;
  content: string;
  media: File | null;
}

const PostPreview: React.FC<PostPreviewProps> = ({ title, content, media }) => {
  return (
    <div className="border rounded-lg p-4">
      <h2 className="text-2xl font-bold mb-4">{title}</h2>
      <div
        className="prose max-w-none"
        dangerouslySetInnerHTML={{ __html: content }}
      />
      {media && (
        <div className="mt-4">
          {media.type.startsWith('image/') ? (
            <img src={URL.createObjectURL(media)} alt="Preview" className="max-w-full h-auto" />
          ) : (
            <video src={URL.createObjectURL(media)} controls className="max-w-full h-auto" />
          )}
        </div>
      )}
    </div>
  );
};

export default PostPreview;