export const mockProfile = {
  avatarUrl: 'https://randomuser.me/api/portraits/men/32.jpg',
  name: 'John Doe',
  title: 'Software Engineer',
  location: 'San Francisco, CA',
  socialLinks: [
    { platform: 'LinkedIn', url: 'https://linkedin.com/in/johndoe' },
    { platform: 'GitHub', url: 'https://github.com/johndoe' },
  ],
  bio: 'Passionate developer with 5+ years of experience in web technologies.',
  skills: ['React', 'TypeScript', 'Node.js', 'SQL'],
  languages: ['English', 'Spanish'], // Added for edit compatibility
  experience: [
    {
      company: 'Tech Corp',
      title: 'Frontend Developer',
      start: '2019',
      end: '2022',
    },
    {
      company: 'Web Solutions',
      title: 'Junior Developer',
      start: '2017',
      end: '2019',
    },
  ],
  education: [
    {
      school: 'State University',
      degree: 'B.Sc. Computer Science',
      start: '2013',
      end: '2017',
    },
  ],
  contact: {
    email: 'john.doe@example.com',
    phone: '+1 555-1234',
  },
  activity: [
    { type: 'post', content: 'Shared a new project on GitHub', date: '2025-07-01' },
    { type: 'connection', content: 'Connected with Jane Smith', date: '2025-06-28' },
  ],
  connections: 120,
  mutualConnections: 8,
};
