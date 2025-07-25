import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { profileApi } from './api';
import { postsApi } from '../posts/api';
import PostList from '../posts/PostList';
import type { Post } from '../../types';

const PROFILE_CACHE_KEY = 'profile_cache';

const ProfileView: React.FC = () => {
  const [profile, setProfile] = useState<any | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [offline, setOffline] = useState(!navigator.onLine);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleOnline = () => setOffline(false);
    const handleOffline = () => setOffline(true);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  useEffect(() => {
    (async () => {
      setLoading(true);
      setError('');

      if (offline) {
        const cachedProfile = localStorage.getItem(PROFILE_CACHE_KEY);
        if (cachedProfile) {
          setProfile(JSON.parse(cachedProfile));
          setError('Offline: showing cached profile.');
        } else {
          setError('You are offline and no cached profile is available.');
        }
        setLoading(false);
        return;
      }

      try {
        // Try the authenticated endpoint first
        const profileData = await profileApi.getProfile();
        if (profileData && profileData.name) {
          setProfile(profileData);
          localStorage.setItem(PROFILE_CACHE_KEY, JSON.stringify(profileData));
          const userPosts = await postsApi.getPostsByUser(profileData.id);
          setPosts(userPosts);
        } else {
          setError('Profile not found.');
        }
      } catch (err) {
        console.log('[DEBUG] Auth endpoint failed, trying test endpoint...');
        try {
          // Fallback to test endpoint if auth fails
          const profileData = await profileApi.getProfileTest();
          if (profileData && profileData.name) {
            setProfile(profileData);
            localStorage.setItem(PROFILE_CACHE_KEY, JSON.stringify(profileData));
            const userPosts = await postsApi.getPostsByUser(profileData.id);
            setPosts(userPosts);
          } else {
            setError('Profile not found.');
          }
        } catch (testErr) {
          setError('Could not fetch profile. Please try again later.');
        }
      } finally {
        setLoading(false);
      }
    })();
  }, [location]);

  const getAvatarUrl = (url: string) => {
    if (!url) return '';
    if (url.startsWith('http://') || url.startsWith('https://')) return url;
    // Add cache buster to force reload after update
    return `http://localhost:5000${url}?cb=${Date.now()}`;
  };

  if (loading) return <div className="text-center py-10">Loading profile...</div>;
  if (error) return (
    <div className="text-center py-10 text-red-500">
      {error}
      <div className="mt-4 text-xs text-gray-400">
        <div>Token: {localStorage.getItem('token') ? 'Present (may be expired)' : 'No token found'}</div>
        <div>API Response: {error}</div>
        <div className="mt-4 space-x-2">
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            onClick={() => {
              localStorage.removeItem('token');
              window.location.href = '/login';
            }}
          >
            Log in again
          </button>
          <button
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            onClick={() => window.location.reload()}
          >
            Refresh Page
          </button>
        </div>
      </div>
    </div>
  );
  if (!profile) return null;

  return (
    <div className="max-w-6xl mx-auto p-4">
      {/* Header Section: avatar left, details center, edit right */}
      <div className="flex flex-row items-center justify-between mb-8 bg-white rounded-lg shadow p-6">
        {/* Avatar */}
        <div className="flex-shrink-0">
          <div className="w-28 h-28 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden border-4 border-white shadow">
            {profile.avatarUrl && (
              <img src={getAvatarUrl(profile.avatarUrl)} alt="Profile" className="object-cover w-full h-full" />
            )}
          </div>
        </div>
        {/* Name and Details */}
        <div className="flex flex-col flex-grow ml-6 min-w-0">
          <h2 className="text-2xl font-bold truncate">{profile.name || 'No Name'}</h2>
          <div className="text-gray-600 truncate">{profile.title || 'No Title'}</div>
          <div className="text-gray-500 text-sm truncate flex items-center">
            <span className="material-icons text-gray-400 mr-1" title="Location">location_on</span>
            <span>{profile.location || 'No Location'}</span>
          </div>
          {/* Add social links here if needed */}
        </div>
        {/* Edit Button and Go to Feed Button */}
        <div className="flex-shrink-0 flex flex-col gap-2 items-end">
          <button
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 mb-2"
            onClick={() => navigate('/profile/edit')}
          >
            Edit Profile
          </button>
          <button
            className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            onClick={() => navigate('/feed')}
          >
            Go to Feed
          </button>
        </div>
      </div>
      {/* Only render the rest if profile has a name or title or bio */}
      {(profile.name || profile.title || profile.bio) && (
        <div className="grid md:grid-cols-3 gap-6">
          {/* Left/Main Column */}
          <div className="md:col-span-2 flex flex-col gap-4">
            <div className="bg-white rounded shadow p-4">
              <h3 className="font-semibold mb-2">About</h3>
              <div>{profile.bio || 'No bio provided.'}</div>
            </div>
            <div className="bg-white rounded shadow p-4">
              <h3 className="font-semibold mb-2">Skills</h3>
              <div className="flex flex-wrap gap-2">
                {profile.skills?.length ? profile.skills.map((skill: string, i: number) => (
                  <span key={i} className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-sm">{skill}</span>
                )) : <span>No skills listed.</span>}
              </div>
            </div>
            <div className="bg-white rounded shadow p-4">
              <h3 className="font-semibold mb-2">Education</h3>
              {profile.education?.length ? (
                <div className="flex flex-col gap-3">
                  {profile.education.map((edu: any, i: number) => (
                    <div key={i} className="border-l-4 border-blue-200 pl-4 pb-2">
                      <div className="font-semibold text-black">
                        {edu.degree}
                      </div>
                      <div className="text-gray-700">
                        {edu.school}
                      </div>
                      <div className="text-sm text-gray-500 mt-1">
                        {edu.start} - {edu.end}
                      </div>
                    </div>
                  ))}
                </div>
              ) : <div>No education info.</div>}
            </div>
            <div className="bg-white rounded shadow p-4">
              <h3 className="font-semibold mb-2">Recent Activity</h3>
              {profile.activity?.length ? (
                profile.activity.slice(0, 5).map((act: any, i: number) => (
                  <div key={i} className="mb-2">
                    <div className="flex justify-between items-center font-semibold">
                      <span>{act.type}</span>
                      <span className="text-xs text-gray-500 ml-2 whitespace-nowrap">{act.date}</span>
                    </div>
                    <div>{act.content}</div>
                  </div>
                ))
              ) : (
                <div>No recent activity.</div>
              )}
              {profile.activity?.length > 5 && <div className="text-blue-600 mt-2">Show more activity</div>}
            </div>
            <div className="bg-white rounded shadow p-4">
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-semibold">Posts</h3>
                <button
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                  onClick={() => navigate('/posts/create')}
                >
                  Create Post
                </button>
              </div>
              <PostList posts={posts} showUsername={false} />
            </div>
          </div>
          {/* Right Column */}
          <div className="flex flex-col gap-4">
            <div className="bg-white rounded shadow p-4">
              <h3 className="font-semibold mb-2">Contact Information</h3>
              <div className="flex items-center mb-1">
                <span className="material-icons text-gray-500 mr-2" title="Email">email</span>
                <span>{profile.contact?.email}</span>
              </div>
              <div className="flex items-center mb-1">
                <span className="material-icons text-gray-500 mr-2" title="Phone">phone</span>
                <span>{profile.contact?.phone}</span>
              </div>
              <div className="flex items-center">
                <span className="material-icons text-gray-500 mr-2" title="Location">location_on</span>
                <span>{profile.location}</span>
              </div>
            </div>
            <div className="bg-white rounded shadow p-4">
              <h3 className="font-semibold mb-2">Languages</h3>
              {profile.languages?.length ? (
                <ul className="list-disc ml-5">
                  {profile.languages.map((lang: string, i: number) => (
                    <li key={i}>{lang}</li>
                  ))}
                </ul>
              ) : <div>No languages listed.</div>}
            </div>
            <div className="bg-white rounded shadow p-4">
              <h3 className="font-semibold mb-2">Connections</h3>
              <div className="flex flex-row items-center justify-between">
                <div className="text-lg font-bold">{profile.connections || 0}+
                  <div className="text-sm text-gray-600 font-normal">Connections</div>
                </div>
                <div className="text-lg font-bold">{profile.mutualConnections || 0}
                  <div className="text-sm text-gray-600 font-normal">Mutual</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      {offline && (
        <div className="text-yellow-600 text-center mt-4">You are offline. Displaying cached profile data.</div>
      )}
    </div>
  );
};

export default ProfileView;