import { Card, CardContent, Typography, Grid, Box, List, ListItem, ListItemText } from '@mui/material';
import { useState, useEffect } from 'react';

export default function Investments() {
  const [stocks, setStocks] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/stocks')
      .then(response => response.json())
      .then(data => {
        setStocks(data.tickers);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching stocks:', error);
        setLoading(false);
      });
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Investment Performance
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Portfolio Overview
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Value: $0.00
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Gain/Loss: $0.00 (0.00%)
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Stock Tickers
              </Typography>
              {loading ? (
                <Typography variant="body2" color="text.secondary">
                  Loading stocks...
                </Typography>
              ) : (
                <List dense>
                  {stocks.map((ticker) => (
                    <ListItem key={ticker}>
                      <ListItemText primary={ticker} />
                    </ListItem>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Holdings
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Add your first investment to get started
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}