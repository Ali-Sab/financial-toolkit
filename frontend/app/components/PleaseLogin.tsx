import { Box, Typography, Card, CardContent } from '@mui/material';

export function PleaseLogin() {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      <Card sx={{ maxWidth: 500, width: '100%' }}>
        <CardContent sx={{ textAlign: 'center', py: 6 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Please Log In
          </Typography>
          <Typography variant="body1" color="text.secondary">
            You need to log in to access your financial dashboard.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
