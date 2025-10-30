import { Box, Card, CardContent, Typography, Chip, Grid, List, ListItem, ListItemText, TextField, Collapse, IconButton, Button } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import { useState, useEffect } from 'react';
import { api } from '~/utils/api';
import { useAuth } from '~/contexts/AuthContext';
import { PleaseLogin } from '~/components/PleaseLogin';

interface Account {
  id: number;
  account_name: string;
  account_type: string;
}

interface Sell {
  id: number;
  stock: string;
  date: string;
  shares: number;
  transaction_amount: number;
  profit: number;
  proceeds: number;
  adjusted_cost: number;
}

export default function Investments() {
  const { user } = useAuth();
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);
  const [sells, setSells] = useState<Sell[]>([]);
  const [netProfit, setNetProfit] = useState<number>(0);
  const [profitByYear, setProfitByYear] = useState<{year: number, profit: number}[]>([]);
  const [profitByMonth, setProfitByMonth] = useState<{year: number, month: number, profit: number}[]>([]);
  const [profitByStock, setProfitByStock] = useState<{stock: string, profit: number}[]>([]);
  const [loading, setLoading] = useState(true);
  const [stockFilter, setStockFilter] = useState('');
  const [expandedYear, setExpandedYear] = useState<number | null>(null);
  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  const [selectedMonth, setSelectedMonth] = useState<number | null>(null);

  useEffect(() => {
    if (!user) {
      setLoading(false);
      return;
    }

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
    fetchAccounts();
  }, [user]);

  useEffect(() => {
    if (!selectedAccount) return;

    const fetchSellsData = async () => {
      try {
        const [sellsData, profitData, yearData, monthData, stockData] = await Promise.all([
          api.get<Sell[]>(`/accounts/${selectedAccount.id}/sells`),
          api.get<{ net_profit: number }>(`/accounts/${selectedAccount.id}/net-profit`),
          api.get<{year: number, profit: number}[]>(`/accounts/${selectedAccount.id}/net-profit/by-year`),
          api.get<{year: number, month: number, profit: number}[]>(`/accounts/${selectedAccount.id}/net-profit/by-month`),
          api.get<{stock: string, profit: number}[]>(`/accounts/${selectedAccount.id}/net-profit/by-stock`)
        ]);
        setSells(sellsData);
        setNetProfit(profitData.net_profit);
        setProfitByYear(yearData);
        setProfitByMonth(monthData);
        setProfitByStock(stockData);
      } catch (error) {
        console.error('Error fetching sells data:', error);
      }
    };
    fetchSellsData();
  }, [selectedAccount]);

  const getFilteredSells = () => {
    let filtered = sells;
    
    if (stockFilter) {
      filtered = filtered.filter(sell => 
        sell.stock.toLowerCase().includes(stockFilter.toLowerCase())
      );
    }
    
    if (selectedYear !== null) {
      filtered = filtered.filter(sell => 
        new Date(sell.date).getFullYear() === selectedYear
      );
    }
    
    if (selectedMonth !== null) {
      filtered = filtered.filter(sell => 
        new Date(sell.date).getMonth() + 1 === selectedMonth
      );
    }
    
    return filtered;
  };

  const getMonthsForYear = (year: number) => {
    return profitByMonth.filter(m => m.year === year);
  };

  if (!user) {
    return <PleaseLogin />;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Investments
      </Typography>

      <Box sx={{ display: 'flex', gap: 2, overflowX: 'auto', pb: 2, mb: 3 }}>
        {loading ? (
          <Typography variant="body2" color="text.secondary">
            Loading accounts...
          </Typography>
        ) : accounts.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            No accounts found.
          </Typography>
        ) : (
          accounts.map((account) => (
            <Chip
              key={account.id}
              label={account.account_name}
              onClick={() => setSelectedAccount(account)}
              color={selectedAccount?.id === account.id ? 'primary' : 'default'}
              sx={{ minWidth: 'fit-content' }}
            />
          ))
        )}
      </Box>

      {selectedAccount ? (
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Years
                </Typography>
                <List>
                  {profitByYear.map((yearItem) => (
                    <Box key={yearItem.year}>
                      <ListItem
                        button
                        onClick={() => setExpandedYear(expandedYear === yearItem.year ? null : yearItem.year)}
                      >
                        <ListItemText
                          primary={yearItem.year}
                          secondary={`$${yearItem.profit.toFixed(2)}`}
                        />
                        <IconButton size="small">
                          {expandedYear === yearItem.year ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                        </IconButton>
                      </ListItem>
                      <Collapse in={expandedYear === yearItem.year}>
                        <List dense sx={{ pl: 4 }}>
                          {getMonthsForYear(yearItem.year).map((monthItem) => (
                            <ListItem
                              key={`${monthItem.year}-${monthItem.month}`}
                              button
                              selected={selectedYear === monthItem.year && selectedMonth === monthItem.month}
                              onClick={() => {
                                setSelectedYear(monthItem.year);
                                setSelectedMonth(monthItem.month);
                              }}
                            >
                              <ListItemText
                                primary={new Date(monthItem.year, monthItem.month - 1).toLocaleString('default', { month: 'long' })}
                                secondary={`$${monthItem.profit.toFixed(2)}`}
                              />
                            </ListItem>
                          ))}
                        </List>
                      </Collapse>
                    </Box>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Sells
                  </Typography>
                  {(selectedYear || selectedMonth) && (
                    <Button size="small" onClick={() => { setSelectedYear(null); setSelectedMonth(null); }}>
                      Clear
                    </Button>
                  )}
                </Box>
                <TextField
                  fullWidth
                  size="small"
                  label="Filter by stock"
                  value={stockFilter}
                  onChange={(e) => setStockFilter(e.target.value)}
                  sx={{ mb: 2 }}
                />
                {getFilteredSells().length === 0 ? (
                  <Typography variant="body2" color="text.secondary">
                    No sells found
                  </Typography>
                ) : (
                  <List>
                    {getFilteredSells().map((sell) => (
                      <ListItem key={sell.id}>
                        <ListItemText
                          primary={`${sell.stock} - ${sell.shares} shares`}
                          secondary={`Profit: $${sell.profit.toFixed(2)} | Date: ${new Date(sell.date).toLocaleDateString()}`}
                        />
                      </ListItem>
                    ))}
                  </List>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Net Profit
                </Typography>
                <Typography variant="h4" color={netProfit >= 0 ? 'success.main' : 'error.main'}>
                  ${netProfit.toFixed(2)}
                </Typography>
                
                <Typography variant="subtitle1" sx={{ mt: 3, mb: 1 }}>
                  By Year
                </Typography>
                <List dense>
                  {profitByYear.map((item) => (
                    <ListItem key={item.year}>
                      <ListItemText
                        primary={item.year}
                        secondary={`$${item.profit.toFixed(2)}`}
                      />
                    </ListItem>
                  ))}
                </List>
                
                <Typography variant="subtitle1" sx={{ mt: 2, mb: 1 }}>
                  By Stock
                </Typography>
                <List dense>
                  {profitByStock.map((item) => (
                    <ListItem key={item.stock}>
                      <ListItemText
                        primary={item.stock}
                        secondary={`$${item.profit.toFixed(2)}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      ) : (
        <Card>
          <CardContent sx={{ minHeight: 400 }}>
            <Typography variant="body2" color="text.secondary">
              Select an account to view details
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}
