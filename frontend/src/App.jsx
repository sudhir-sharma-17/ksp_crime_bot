import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import LoginPage from './components/auth/LoginPage';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [officerProfile, setOfficerProfile] = useState(null);

  const handleLoginSuccess = (profile) => {
    setOfficerProfile(profile);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setOfficerProfile(null);
  };

  if (!isAuthenticated) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <Dashboard 
      officerProfile={officerProfile} 
      onLogout={handleLogout} 
    />
  );
}

export default App;
