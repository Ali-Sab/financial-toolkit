import { Card, CardContent, Typography, Grid, Box, List, ListItem, ListItemText, Button, Modal, TextField, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import DeleteIcon from '@mui/icons-material/Delete';
import { useState, useEffect } from 'react';
import { api } from '~/utils/api';
import { useAuth } from '~/contexts/AuthContext';
import { PleaseLogin } from '~/components/PleaseLogin';

interface Account {
  id: number;
  account_name: string;
  account_type: string;
}

export default function Investments() {
  const { user } = useAuth();
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [createOpen, setCreateOpen] = useState(false);
  const [uploadOpen, setUploadOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);
  const [accountToDelete, setAccountToDelete] = useState<Account | null>(null);
  const [accountName, setAccountName] = useState('');
  const [accountType, setAccountType] = useState('');
  const [zipFile, setZipFile] = useState<File | null>(null);
  const [error, setError] = useState('');

  const fetchAccounts = async () => {
    try {
      const data = await api.get<Account[]>('/accounts');
      setAccounts(data);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!user) {
      setLoading(false);
      return;
    }
    fetchAccounts();
  }, [user]);

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/accounts', { account_name: accountName, account_type: accountType });
      await fetchAccounts();
      setCreateOpen(false);
      setAccountName('');
      setAccountType('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create account');
    }
  };

  const handleUpload = async () => {
    if (!zipFile || !selectedAccount) return;
    
    setError('');
    try {
      await api.uploadFile(`/process-stock-transactions/${selectedAccount.id}`, zipFile);
      setUploadOpen(false);
      setZipFile(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload file');
    }
  };

  const handleDeleteAccount = async () => {
    if (!accountToDelete) return;
    
    try {
      await api.delete(`/accounts/${accountToDelete.id}`);
      await fetchAccounts();
      setDeleteOpen(false);
      setAccountToDelete(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete account');
    }
  };

  if (!user) {
    return <PleaseLogin />;
  }

  return (
    <>
      <Box sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Accounts
          </Typography>
          <Button variant="contained" onClick={() => setCreateOpen(true)}>
            Create Account
          </Button>
        </Box>
        
        <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Financial Accounts
              </Typography>
              {loading ? (
                <Typography variant="body2" color="text.secondary">
                  Loading accounts...
                </Typography>
              ) : accounts.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No accounts found. Create your first account to get started.
                </Typography>
              ) : (
                <List>
                  {accounts.map((account) => (
                    <ListItem 
                      key={account.id}
                      secondaryAction={
                        <IconButton 
                          edge="end" 
                          onClick={(e) => {
                            e.stopPropagation();
                            setAccountToDelete(account);
                            setDeleteOpen(true);
                          }}
                        >
                          <DeleteIcon />
                        </IconButton>
                      }
                      button
                      onClick={() => {
                        setSelectedAccount(account);
                        setUploadOpen(true);
                      }}
                      sx={{ 
                        '&:hover': { 
                          backgroundColor: 'action.hover',
                          cursor: 'pointer'
                        }
                      }}
                    >
                      <ListItemText 
                        primary={account.account_name}
                        secondary={account.account_type}
                      />
                    </ListItem>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
          </Grid>
        </Grid>
      </Box>

      <Modal open={uploadOpen} onClose={() => setUploadOpen(false)}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }} onClick={() => setUploadOpen(false)}>
          <Card sx={{ maxWidth: 400, width: '100%' }} onClick={(e) => e.stopPropagation()}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h5" component="h1">
                  Upload to {selectedAccount?.account_name}
                </Typography>
                <IconButton onClick={() => setUploadOpen(false)} size="small">
                  <CloseIcon />
                </IconButton>
              </Box>
              <Box sx={{ mt: 2 }}>
                <Button
                  variant="outlined"
                  component="label"
                  fullWidth
                >
                  {zipFile ? zipFile.name : 'Select ZIP File'}
                  <input
                    type="file"
                    accept=".zip"
                    hidden
                    onChange={(e) => setZipFile(e.target.files?.[0] || null)}
                  />
                </Button>
                {error && (
                  <Typography color="error" variant="body2" sx={{ mt: 1 }}>
                    {error}
                  </Typography>
                )}
                <Button 
                  variant="contained" 
                  fullWidth 
                  sx={{ mt: 2 }}
                  disabled={!zipFile}
                  onClick={handleUpload}
                >
                  Upload
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Box>
      </Modal>

      <Modal open={createOpen} onClose={() => setCreateOpen(false)}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }} onClick={() => setCreateOpen(false)}>
          <Card sx={{ maxWidth: 400, width: '100%' }} onClick={(e) => e.stopPropagation()}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h5" component="h1">
                  Create Account
                </Typography>
                <IconButton onClick={() => setCreateOpen(false)} size="small">
                  <CloseIcon />
                </IconButton>
              </Box>
              <form onSubmit={handleCreateAccount}>
                <TextField
                  fullWidth
                  label="Account Name"
                  value={accountName}
                  onChange={(e) => setAccountName(e.target.value)}
                  margin="normal"
                  required
                />
                <TextField
                  fullWidth
                  label="Account Type"
                  value={accountType}
                  onChange={(e) => setAccountType(e.target.value)}
                  margin="normal"
                  required
                />
                {error && (
                  <Typography color="error" variant="body2" sx={{ mt: 1 }}>
                    {error}
                  </Typography>
                )}
                <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>
                  Create
                </Button>
              </form>
            </CardContent>
          </Card>
        </Box>
      </Modal>

      <Modal open={deleteOpen} onClose={() => setDeleteOpen(false)}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }} onClick={() => setDeleteOpen(false)}>
          <Card sx={{ maxWidth: 400, width: '100%' }} onClick={(e) => e.stopPropagation()}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h5" component="h1">
                  Delete Account
                </Typography>
                <IconButton onClick={() => setDeleteOpen(false)} size="small">
                  <CloseIcon />
                </IconButton>
              </Box>
              <Typography variant="body1" sx={{ mt: 2 }}>
                Are you sure you want to delete "{accountToDelete?.account_name}"? This action cannot be undone.
              </Typography>
              {error && (
                <Typography color="error" variant="body2" sx={{ mt: 1 }}>
                  {error}
                </Typography>
              )}
              <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
                <Button variant="outlined" fullWidth onClick={() => setDeleteOpen(false)}>
                  Cancel
                </Button>
                <Button variant="contained" color="error" fullWidth onClick={handleDeleteAccount}>
                  Delete
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Box>
      </Modal>
    </>
  );
}