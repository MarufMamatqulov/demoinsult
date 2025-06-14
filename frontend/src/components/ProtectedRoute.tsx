import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
  redirectPath?: string;
  children?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  redirectPath = '/login',
  children
}) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    // While we're checking authentication status, show a loading indicator
    return (
      <div className="loading-container">
        <div className="loader"></div>
        <p>Loading...</p>
      </div>
    );
  }
  
  // If not authenticated, redirect to the login page
  if (!isAuthenticated) {
    return <Navigate to={redirectPath} replace />;
  }
  
  // If authenticated, render the children or the outlet
  return children ? <>{children}</> : <Outlet />;
};

export default ProtectedRoute;
