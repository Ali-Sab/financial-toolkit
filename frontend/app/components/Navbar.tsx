import { AppBar, Toolbar, Button, Typography, Box, Modal, Card, CardContent, TextField, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { Link } from "react-router";
import { useState } from 'react';
import { api } from '~/utils/api';
import { useAuth } from '~/contexts/AuthContext';

export function Navbar() {
  const { user, setUser, refreshUser } = useAuth();
  const [loginOpen, setLoginOpen] = useState(false);
  const [registerOpen, setRegisterOpen] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/auth/login', { email, password });
      await refreshUser();
      setLoginOpen(false);
      setEmail('');
      setPassword('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/auth/register', { email, username, password });
      await refreshUser();
      setRegisterOpen(false);
      setEmail('');
      setUsername('');
      setPassword('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    }
  };

  const handleLogout = async () => {
    try {
      await api.post('/auth/logout');
      setUser(null);
    } catch (err) {
      console.error('Logout failed');
    }
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ mr: 2 }}>
            Financial Toolkit
          </Typography>
          {user && (
            <>
              <Button color="inherit" component={Link} to="/">
                Dashboard
              </Button>
              <Button color="inherit" component={Link} to="/investment-performance">
                Investments
              </Button>
            </>
          )}
          <Box sx={{ flexGrow: 1 }} />
          {user ? (
            <>
              <Typography variant="body1" sx={{ mr: 2 }}>
                Logged in as {user.username}
              </Typography>
              <Button color="inherit" onClick={handleLogout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button color="inherit" onClick={() => setLoginOpen(true)}>
                Login
              </Button>
              <Button color="inherit" onClick={() => setRegisterOpen(true)}>
                Register
              </Button>
            </>
          )}
        </Toolbar>
      </AppBar>

      <Modal open={loginOpen} onClose={() => setLoginOpen(false)}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }} onClick={() => setLoginOpen(false)}>
          <Card sx={{ maxWidth: 400, width: '100%' }} onClick={(e) => e.stopPropagation()}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h5" component="h1">
                  Login
                </Typography>
                <IconButton onClick={() => setLoginOpen(false)} size="small">
                  <CloseIcon />
                </IconButton>
              </Box>
              <form onSubmit={handleLogin}>
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  margin="normal"
                  required
                />
                <TextField
                  fullWidth
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  margin="normal"
                  required
                />
                {error && (
                  <Typography color="error" variant="body2" sx={{ mt: 1 }}>
                    {error}
                  </Typography>
                )}
                <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>
                  Login
                </Button>
              </form>
            </CardContent>
          </Card>
        </Box>
      </Modal>

      <Modal open={registerOpen} onClose={() => setRegisterOpen(false)}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }} onClick={() => setRegisterOpen(false)}>
          <Card sx={{ maxWidth: 400, width: '100%' }} onClick={(e) => e.stopPropagation()}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h5" component="h1">
                  Register
                </Typography>
                <IconButton onClick={() => setRegisterOpen(false)} size="small">
                  <CloseIcon />
                </IconButton>
              </Box>
              <form onSubmit={handleRegister}>
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  margin="normal"
                  required
                />
                <TextField
                  fullWidth
                  label="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  margin="normal"
                  required
                />
                <TextField
                  fullWidth
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  margin="normal"
                  required
                />
                {error && (
                  <Typography color="error" variant="body2" sx={{ mt: 1 }}>
                    {error}
                  </Typography>
                )}
                <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>
                  Register
                </Button>
              </form>
            </CardContent>
          </Card>
        </Box>
      </Modal>
    </>
  );
}