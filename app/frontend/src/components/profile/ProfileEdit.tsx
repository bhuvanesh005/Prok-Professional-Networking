import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ProfileFormInput from './ProfileFormInput';
import ProfileImageUpload from './ProfileImageUpload';
import { mockProfile } from './mockProfileData';
import { profileApi } from './api';

const initialState = {
  avatarUrl: '',
  name: '',
  title: '',
  location: '',
  bio: '',
  skills: '',
  email: '',
  phone: '',
  languages: '',
  connections: '',
  mutualConnections: '',
  education: [] as { school: string; degree: string; start: string; end: string }[],
  activity: [] as { type: string; content: string; date: string }[],
};

const ProfileEdit: React.FC = () => {
  const [form, setForm] = useState(initialState);
  const [errors, setErrors] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [education, setEducation] = useState<any[]>([]);
  const [activity, setActivity] = useState<any[]>([]);
  const [avatarCacheBuster, setAvatarCacheBuster] = useState(Date.now());
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch profile data (mock or real)
    (async () => {
      try {
        const data = await profileApi.getProfile();
        setForm({
          avatarUrl: data.avatarUrl || '',
          name: data.name || '',
          title: data.title || '',
          location: data.location || '',
          bio: data.bio || '',
          skills: (data.skills || []).join(', '),
          email: data.contact?.email || '',
          phone: data.contact?.phone || '',
          languages: (data.languages || []).join(', '),
          connections: data.connections?.toString() || '',
          mutualConnections: data.mutualConnections?.toString() || '',
          education: data.education || [],
          activity: data.activity || [],
        });
        setAvatarPreview(data.avatarUrl || '');
        setEducation(data.education || []);
        setActivity(data.activity || []);
      } catch {
        setForm({
          avatarUrl: mockProfile.avatarUrl,
          name: mockProfile.name,
          title: mockProfile.title,
          location: mockProfile.location,
          bio: mockProfile.bio,
          skills: mockProfile.skills.join(', '),
          email: mockProfile.contact.email,
          phone: mockProfile.contact.phone,
          languages: (mockProfile.languages || []).join(', '),
          connections: mockProfile.connections?.toString() || '',
          mutualConnections: mockProfile.mutualConnections?.toString() || '',
          education: mockProfile.education || [],
          activity: mockProfile.activity || [],
        });
        setAvatarPreview(mockProfile.avatarUrl);
        setEducation(mockProfile.education || []);
        setActivity(mockProfile.activity || []);
      }
    })();
  }, []);

  const validate = (field = form) => {
    const errs: any = {};
    if (!field.name) errs.name = 'Name is required.';
    if (!field.title) errs.title = 'Title is required.';
    if (!field.location) errs.location = 'Location is required.';
    if (!field.email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(field.email)) errs.email = 'Valid email required.';
    if (field.phone && !/^\+?[\d\s-]+$/.test(field.phone)) errs.phone = 'Invalid phone.';
    if (!field.skills) errs.skills = 'At least one skill required.';
    if (!field.languages) errs.languages = 'At least one language required.';
    if (field.connections && isNaN(Number(field.connections))) errs.connections = 'Must be a number.';
    if (field.mutualConnections && isNaN(Number(field.mutualConnections))) errs.mutualConnections = 'Must be a number.';
    return errs;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: undefined });
    setSuccess('');
  };

  const handleImageChange = (file: File | null, error?: string) => {
    setAvatarFile(file);
    setSuccess('');
    if (file && !error) {
      setAvatarPreview(URL.createObjectURL(file));
      setErrors((prev: any) => ({ ...prev, avatar: undefined }));
      setAvatarCacheBuster(Date.now()); // Update cache buster on new image
    } else if (error) {
      setAvatarPreview(form.avatarUrl);
      setErrors((prev: any) => ({ ...prev, avatar: error }));
    } else {
      setAvatarPreview(form.avatarUrl);
    }
  };

  const handleEducationChange = (idx: number, field: string, value: string) => {
    setEducation(education => education.map((edu, i) => i === idx ? { ...edu, [field]: value } : edu));
  };
  const handleAddEducation = () => {
    setEducation([...education, { school: '', degree: '', start: '', end: '' }]);
  };
  const handleRemoveEducation = (idx: number) => {
    setEducation(education => education.filter((_, i) => i !== idx));
  };

  const handleActivityChange = (idx: number, field: string, value: string) => {
    setActivity(activity => activity.map((act, i) => i === idx ? { ...act, [field]: value } : act));
  };
  const handleAddActivity = () => {
    setActivity([...activity, { type: '', content: '', date: '' }]);
  };
  const handleRemoveActivity = (idx: number) => {
    setActivity(activity => activity.filter((_, i) => i !== idx));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) {
      setErrors(errs);
      return;
    }
    setLoading(true);
    setSuccess('');
    try {
      let avatarUrl = form.avatarUrl;
      if (avatarFile) {
        setUploading(true);
        setProgress(30);
        // Upload the image to backend
        const uploadRes = await profileApi.uploadProfileImage(avatarFile);
        if (uploadRes && uploadRes.imageUrl) {
          avatarUrl = uploadRes.imageUrl;
          setAvatarPreview(avatarUrl);
          setAvatarCacheBuster(Date.now());
        } else if (uploadRes && uploadRes.message) {
          setErrors((prev: any) => ({ ...prev, avatar: uploadRes.message }));
          setUploading(false);
          setLoading(false);
          return;
        }
        setProgress(100);
        setUploading(false);
      }
      const payload = {
        ...form,
        avatarUrl,
        skills: form.skills.split(',').map((s) => s.trim()),
        languages: form.languages.split(',').map((l) => l.trim()),
        connections: Number(form.connections),
        mutualConnections: Number(form.mutualConnections),
        contact: { email: form.email, phone: form.phone },
        education: education.map(e => ({
          school: e.school,
          degree: e.degree,
          start: e.start,
          end: e.end,
        })),
        activity: activity.map(a => ({
          type: a.type,
          content: a.content,
          date: a.date,
        })),
      };
      await profileApi.updateProfile(payload);
      localStorage.removeItem('profile_cache'); // Clear cache so profile page fetches fresh data
      // Re-fetch profile to update avatar and all fields
      const updated = await profileApi.getProfile();
      setForm({
        avatarUrl: updated.avatarUrl || '',
        name: updated.name || '',
        title: updated.title || '',
        location: updated.location || '',
        bio: updated.bio || '',
        skills: (updated.skills || []).join(', '),
        email: updated.contact?.email || '',
        phone: updated.contact?.phone || '',
        languages: (updated.languages || []).join(', '),
        connections: updated.connections?.toString() || '',
        mutualConnections: updated.mutualConnections?.toString() || '',
        education: updated.education || [],
        activity: updated.activity || [],
      });
      setAvatarPreview(updated.avatarUrl || '');
      setEducation(updated.education || []);
      setActivity(updated.activity || []);
      setSuccess('Profile updated successfully!');
      setTimeout(() => navigate('/profile'), 800); // Go back after save
    } catch {
      setErrors({ submit: 'Failed to update profile.' });
    }
    setLoading(false);
  };

  function isBlobUrl(url: string | null): boolean {
    return !!url && url.startsWith('blob:');
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center mb-4">
          <button
            type="button"
            className="mr-4 px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
            onClick={() => navigate('/profile')}
          >
            ← Back
          </button>
          <h1 className="text-2xl font-bold">Edit Profile</h1>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="relative flex justify-center mb-4">
            <ProfileImageUpload
              imageUrl={avatarPreview ? (isBlobUrl(avatarPreview) ? avatarPreview : `${avatarPreview}?cb=${avatarCacheBuster}`) : null}
              onImageChange={handleImageChange}
              uploading={uploading}
              progress={progress}
            />
            <span className="absolute bottom-2 right-2 bg-blue-600 text-white rounded-full p-2 shadow cursor-pointer" style={{ pointerEvents: 'none' }}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536M9 13h3l8-8a2.828 2.828 0 00-4-4l-8 8v3h3z" /></svg>
            </span>
          </div>
          {errors.avatar && <div className="text-red-500 text-xs text-center mb-2">{errors.avatar}</div>}
          <div className="grid md:grid-cols-2 gap-4">
            <ProfileFormInput label="Name" name="name" value={form.name} onChange={handleChange} error={errors.name} />
            <ProfileFormInput label="Title" name="title" value={form.title} onChange={handleChange} error={errors.title} />
            <ProfileFormInput label="Location" name="location" value={form.location} onChange={handleChange} error={errors.location} />
            <ProfileFormInput label="Email" name="email" value={form.email} onChange={handleChange} error={errors.email} type="email" />
            <ProfileFormInput label="Phone" name="phone" value={form.phone} onChange={handleChange} error={errors.phone} type="tel" />
            <ProfileFormInput label="Skills (comma separated)" name="skills" value={form.skills} onChange={handleChange} error={errors.skills} />
            <ProfileFormInput label="Languages (comma separated)" name="languages" value={form.languages} onChange={handleChange} error={errors.languages} />
            <ProfileFormInput label="Connections" name="connections" value={form.connections} onChange={handleChange} error={errors.connections} type="number" />
            <ProfileFormInput label="Mutual Connections" name="mutualConnections" value={form.mutualConnections} onChange={handleChange} error={errors.mutualConnections} type="number" />
          </div>
          <ProfileFormInput label="Bio" name="bio" value={form.bio} onChange={handleChange} error={errors.bio} textarea />

          {/* Education Section */}
          <div className="mt-6">
            <h3 className="font-semibold mb-2">Education</h3>
            {education.map((edu, idx) => (
              <div key={idx} className="flex flex-wrap gap-2 mb-2 items-center">
                <input
                  className="border rounded px-2 py-1 w-40"
                  placeholder="School"
                  value={edu.school}
                  onChange={e => handleEducationChange(idx, 'school', e.target.value)}
                />
                <input
                  className="border rounded px-2 py-1 w-40"
                  placeholder="Degree"
                  value={edu.degree}
                  onChange={e => handleEducationChange(idx, 'degree', e.target.value)}
                />
                <input
                  className="border rounded px-2 py-1 w-24"
                  placeholder="Start Year"
                  value={edu.start}
                  onChange={e => handleEducationChange(idx, 'start', e.target.value)}
                />
                <input
                  className="border rounded px-2 py-1 w-24"
                  placeholder="End Year"
                  value={edu.end}
                  onChange={e => handleEducationChange(idx, 'end', e.target.value)}
                />
                <button
                  type="button"
                  className="text-red-500 ml-2"
                  onClick={() => handleRemoveEducation(idx)}
                >Remove</button>
              </div>
            ))}
            <button
              type="button"
              className="mt-2 px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
              onClick={handleAddEducation}
            >
              + Add Education
            </button>
          </div>

          {/* Activity Section */}
          <div className="mt-6">
            <h3 className="font-semibold mb-2">Recent Activity</h3>
            {activity.map((act, idx) => (
              <div key={idx} className="flex flex-wrap gap-2 mb-2 items-center">
                <input
                  className="border rounded px-2 py-1 w-32"
                  placeholder="Type"
                  value={act.type}
                  onChange={e => handleActivityChange(idx, 'type', e.target.value)}
                />
                <input
                  className="border rounded px-2 py-1 w-64"
                  placeholder="Content"
                  value={act.content}
                  onChange={e => handleActivityChange(idx, 'content', e.target.value)}
                />
                <input
                  className="border rounded px-2 py-1 w-32"
                  placeholder="Date"
                  value={act.date}
                  onChange={e => handleActivityChange(idx, 'date', e.target.value)}
                />
                <button
                  type="button"
                  className="text-red-500 ml-2"
                  onClick={() => handleRemoveActivity(idx)}
                >Remove</button>
              </div>
            ))}
            <button
              type="button"
              className="mt-2 px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
              onClick={handleAddActivity}
            >
              + Add Activity
            </button>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 mt-4"
            disabled={loading || uploading}
          >
            {loading ? 'Saving...' : 'Save Changes'}
          </button>
          {errors.submit && <div className="text-red-500 text-center mt-2">{errors.submit}</div>}
          {success && <div className="text-green-600 text-center mt-2">{success}</div>}
        </form>
      </div>
    </div>
  );
};

export default ProfileEdit;