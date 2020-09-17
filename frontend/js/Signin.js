import Avatar from '@material-ui/core/Avatar';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';
import Container from '@material-ui/core/Container';
import CssBaseline from '@material-ui/core/CssBaseline';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Link from '@material-ui/core/Link';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import React, { Component } from 'react';
import { hot } from 'react-hot-loader/root';

function Copyright() {
  return (
    <Typography align="center" color="textSecondary" variant="body2">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

class Signin extends Component {
  render() {
    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={useStyles.paper}>
          <Avatar className={useStyles.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <form className={useStyles.form} noValidate>
            <TextField
              autoComplete="email"
              autoFocus
              fullWidth
              id="email"
              label="Email Address"
              margin="normal"
              name="email"
              required
              variant="outlined"
            />
            <TextField
              autoComplete="current-password"
              fullWidth
              id="password"
              label="Password"
              margin="normal"
              name="password"
              required
              type="password"
              variant="outlined"
            />
            <FormControlLabel
              control={<Checkbox color="primary" value="remember" />}
              label="Remember me"
            />
            <Button
              className={useStyles.submit}
              color="primary"
              fullWidth
              type="submit"
              variant="contained"
            >
              Sign In
            </Button>
          </form>
        </div>
        <Box mt={8}>
          <Copyright />
        </Box>
      </Container>
    );
  }
}

export default hot(Signin);
