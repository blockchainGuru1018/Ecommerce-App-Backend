import AppBar from '@material-ui/core/AppBar';
import Badge from '@material-ui/core/Badge';
import Box from '@material-ui/core/Box';
import CssBaseline from '@material-ui/core/CssBaseline';
import Divider from '@material-ui/core/Divider';
import Drawer from '@material-ui/core/Drawer';
import IconButton from '@material-ui/core/IconButton';
import Link from '@material-ui/core/Link';
import List from '@material-ui/core/List';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import MenuIcon from '@material-ui/icons/Menu';
import NotificationsIcon from '@material-ui/icons/Notifications';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { withRouter } from 'react-router';

import '../../sass/pages/_all.scss';
import { mainListItems } from './listItems';

function Copyright() {
  return (
    <Typography align="center" color="textSecondary" variant="body2">
      {'Copyright © '}
      <Link color="inherit" href="">
        Unboxxen Administrator
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const drawerWidth = 0;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    marginLeft: '165px',
  },
  toolbar: {
    paddingRight: 24, // keep right padding when drawer closed
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing(7),
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing(9),
    },
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    height: '100vh',
    overflow: 'auto',
  },
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
  },
  fixedHeight: {
    height: 240,
  },
}));

class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      setOpen: true,
    };
  }

  handleDrawerOpen() {
    this.setState({ setOpen: true });
  }

  handleDrawerClose() {
    this.setState({ setOpen: false });
  }

  render() {
    const { children } = this.props;
    const { setOpen } = this.state;
    return (
      <div className={useStyles.root}>
        <CssBaseline />
        <AppBar className="root">
          <Toolbar className={useStyles.toolbar}>
            <IconButton
              aria-label="open drawer"
              className="menuButton"
              color="inherit"
              edge="start"
              onClick={this.handleDrawerOpen}
            >
              <MenuIcon />
            </IconButton>
            <Typography
              className={useStyles.title}
              color="inherit"
              component="h1"
              noWrap
              variant="h6"
            >
              Dashboard
            </Typography>
            <IconButton color="inherit">
              <Badge badgeContent={4} color="secondary">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Toolbar>
        </AppBar>
        <Drawer
          classes={{
            paper: clsx(useStyles.drawerPaper, !this.setOpen && useStyles.drawerPaperClose),
          }}
          open={this.setOpen}
          variant="permanent"
        >
          <div className={useStyles.toolbarIcon}>
            <IconButton onClick={this.handleDrawerClose}>
              <ChevronLeftIcon />
            </IconButton>
          </div>
          <Divider />
          <List>{mainListItems}</List>
        </Drawer>
        <main className={useStyles.content}>
          <div className={useStyles.appBarSpacer} />
          <div className="page-container">
            <Paper className="page-paper">{children}</Paper>
          </div>
        </main>
        <div className="page-hooter">
          <Box pt={4}>
            <Copyright />
          </Box>
        </div>
      </div>
    );
  }
}

Dashboard.propTypes = {
  children: PropTypes.element.isRequired,
};
export default withRouter(Dashboard);
