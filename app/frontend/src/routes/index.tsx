import { createBrowserRouter } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import Login from '../components/auth/Login';
import Signup from '../components/auth/Signup';
import ProfileView from '../components/profile/ProfileView';
import ProfileEdit from '../components/profile/ProfileEdit';
import PostCreationForm from '../components/posts/PostCreationForm';
import PostListAdvanced from '../components/posts/PostListAdvanced';
import PostListTest from '../components/posts/PostListTest';
import Feed from '../components/feed/Feed';
import JobList from '../components/job-board/JobList';
import MessageList from '../components/messaging/MessageList';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Login />,
  },
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/signup',
    element: <Signup />,
  },
  {
    path: '/test-posts',
    element: <PostListTest />,
  },
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        path: '/feed',
        element: <Feed />,
      },
      {
        path: '/profile',
        element: <ProfileView />,
      },
      {
        path: '/profile/edit',
        element: <ProfileEdit />,
      },
      {
        path: '/posts',
        element: <PostListAdvanced />,
      },
      {
        path: '/posts/create',
        element: <PostCreationForm />,
      },
      {
        path: '/jobs',
        element: <JobList />,
      },
      {
        path: '/messages',
        element: <MessageList />,
      },
    ],
  },
]); 