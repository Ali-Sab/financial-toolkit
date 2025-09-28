import { AppBar, Toolbar, Button, Typography } from '@mui/material';
import { Link } from "react-router";

export function Navbar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ mr: 2 }}>
          Financial Toolkit
        </Typography>
        <Button color="inherit" component={Link} to="/">
          Dashboard
        </Button>
        <Button color="inherit" component={Link} to="/investment-performance">
          Investments
        </Button>
      </Toolbar>
    </AppBar>
  );
}