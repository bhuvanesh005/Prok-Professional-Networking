import React, { useState } from 'react';
import RichTextEditor from '../common/RichTextEditor';
import PostPreview from './PostPreview';
import { postsApi } from './api';

const PostCreationForm = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [media, setMedia] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPreview, setShowPreview] = useState(false);

  const handleContentChange = (value: string) => {
    setContent(value);
  };

  const handleMediaChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setMedia(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      await postsApi.createPost(title, content, media || undefined);
      setTitle('');
      setContent('');
      setMedia(null);
    } catch (err) {
      setError('Failed to create post. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col p-8 bg-gray-100">
      <div className="flex-1 max-w-4xl mx-auto w-full">
        <h1 className="text-3xl font-bold mb-6">Create a New Post</h1>
        {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="title" className="block text-lg font-semibold text-gray-800 mb-2">
              Post Title
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          <div>
            <label htmlFor="content" className="block text-lg font-semibold text-gray-800 mb-2">
              Post Content
            </label>
            <div className="bg-white rounded-lg shadow">
              <RichTextEditor value={content} onChange={handleContentChange} />
            </div>
          </div>
          <div>
            <label htmlFor="media" className="block text-lg font-semibold text-gray-800 mb-2">
              Upload Media
            </label>
            <div className="flex items-center justify-center w-full">
              <label htmlFor="media" className="flex flex-col items-center justify-center w-full h-48 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-white hover:bg-gray-50">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <svg className="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                  <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                  <p className="text-xs text-gray-500">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
                </div>
                <input id="media" type="file" className="hidden" onChange={handleMediaChange} accept="image/*,video/*" />
              </label>
            </div>
          </div>
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => setShowPreview(true)}
              className="px-8 py-3 bg-gray-600 text-white font-bold rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
            >
              Preview
            </button>
            <button
              type="submit"
              className="px-8 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              disabled={isLoading}
            >
              {isLoading ? 'Publishing...' : 'Publish Post'}
            </button>
          </div>
        </form>
      </div>
      {showPreview && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg shadow-xl p-8 max-w-2xl w-full">
            <h2 className="text-2xl font-bold mb-4">Post Preview</h2>
            <PostPreview title={title} content={content} media={media} />
            <button
              onClick={() => setShowPreview(false)}
              className="mt-6 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
            >
              Close Preview
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PostCreationForm;