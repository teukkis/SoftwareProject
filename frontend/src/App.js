import React, { useState, useEffect } from 'react'

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Container from '@material-ui/core/Container';

import CreateUser from './components/createUser'
import Users from './components/users'
import VMState from './components/vmState'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  vm: {
    height: 320,
  },
  users: {
    height: 695,
  },
  keys: {
    height: 360,
  },
}));

const App = () => {

  const classes = useStyles();

  return (
    <div>
      <Container maxWidth="lg">
        <Grid container spacing={2}>

          <Grid item xs={7}>
            <Grid container spacing={2}>
              
              <Grid item xs={12}>
                <Paper className={classes.vm} elevation={5}>
                  <VMState />
                </Paper>
              </Grid>

              <Grid item xs={12}>
                <Paper className={classes.keys} elevation={5}>
                  <CreateUser/>
                </Paper>
              </Grid>

            </Grid>
          </Grid>

          <Grid item xs={5}>
            <Paper className={classes.users} elevation={5}>
              <Users/>
            </Paper>
          </Grid>

        </Grid>
      </Container>
    </div>
  );
}

export default App;
