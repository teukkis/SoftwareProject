import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'

import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Divider from '@material-ui/core/Divider';

import userService from '../services/userService'
import { setSSH, clearSSH } from '../redux/ssh'
import { addUser } from '../redux/user'


const useStyles = makeStyles((theme) => ({
  genButton: {
    marginTop: 25,
  },
  clearButton: {
    marginTop: 25,
    marginLeft: 10
  },
  privateField: {
    paddingTop: 10,
    marginLeft: 10,
    marginRight: 10
  },
  publicField: {
    marginLeft: 10,
    marginRight: 10
  }
}))


const CreateUser = () => {

  const classes = useStyles();
  const sshKeys = useSelector( state => state.sshReducer)
  const dispatch = useDispatch()

  const generateUser = () => {
    userService
      .createUser()
      .then(response => {
        userService
        .getUser(response.id)
        .then(response => {
          dispatch( setSSH(response) )
          dispatch( addUser(response) )
        })
      }).catch( error => console.log("couldn't generate a new user"))
  }

  const clearFields = () => {
    dispatch( clearSSH() )
  }

  return (
    <div>
      <div>
        <div className={classes.privateField}>
          <TextField 
            id="outlined-static" 
            multiline={true}
            rows={13}
            fullWidth={true}
            value={sshKeys.privateKey}
            variant="outlined"
          />
        </div>
        <Divider light />
        <div className={classes.publicField}>
          <TextField 
            id="outlined-static" 
            variant="filled" 
            multiline={true}
            rows={4}
            fullWidth={true}
            value={sshKeys.publicKey}
          /> 
        </div>
      </div>
      <Button 
        className={classes.genButton} 
        variant="contained"
        onClick={() => generateUser()}
        >
          Generate a user
      </Button>
      <Button 
        className={classes.clearButton} 
        variant="contained"
        onClick={() => clearFields()}
        >
          Clear
      </Button>
    </div>
  )
}

export default CreateUser
