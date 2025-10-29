import { Box, Typography, Card, CardContent } from '@mui/material';
import { useAuth } from '~/contexts/AuthContext';
import { PleaseLogin } from '~/components/PleaseLogin';

export default function Welcome() {
  const { user } = useAuth();

  if (!user) return <PleaseLogin />;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Welcome to Financial Toolkit
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Your personal financial dashboard for tracking investments, capital gains, and portfolio performance.
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Dashboard Overview
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Monitor your financial progress, analyze investment performance, and make informed decisions with comprehensive financial insights.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}