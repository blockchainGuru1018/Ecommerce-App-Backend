import { createBrowserHistory } from 'history';
import { Dashboard, Chart, Orders } from 'pages/index';
import React from 'react';
import { hot } from 'react-hot-loader/root';
import { Router } from 'react-router';
import { Route, Switch } from 'react-router-dom';
import 'bootstrap';
import { ToastContainer } from 'react-toastify';

import '../sass/pages/_all.scss';
import Deposits from './pages/Deposits';
import SignIn from './Signin';

const App = () => (
  <Router history={createBrowserHistory()}>
    <ToastContainer autoClose={5000} position="top-right" style={{ zIndex: 1999 }} />

    <Switch>
      <Route component={SignIn} exact path="/admin/sign-in" />

      <Dashboard>
        <Switch>
          <Route component={Chart} exact path="/admin/products" />
          <Route component={Orders} exact path="/admin/report" />
          <Route component={Deposits} exact path="/admin/users" />
        </Switch>
      </Dashboard>
    </Switch>
  </Router>
);

export default hot(App);
