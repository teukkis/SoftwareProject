import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux'

import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Divider from '@material-ui/core/Divider';
import Modal from '@material-ui/core/Modal';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

import userService from '../services/userService'
import { setSSH, clearSSH } from '../redux/ssh'
import { addUser } from '../redux/user'


const useStyles = makeStyles((theme) => ({
  genButton: {
    marginTop: 10,
  },
  clearButton: {
    marginTop: 10,
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
  },
  btns: {
    marginLeft: 13
  },
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  paper: {
    backgroundColor: theme.palette.background.paper,
    border: '2px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
    width: 300,
  },
  applyButton: {
    marginTop: "10px"
  }
}))


const CreateUser = () => {

  const classes = useStyles();

  const [ newId, setNewId ] = useState('')
  const [ open, setOpen ] = useState(false)
  const sshKeys = useSelector( state => state.sshReducer)
  const dispatch = useDispatch()

  const handleClose = () => {
    setOpen(false);
  };

  const generateUser = () => {
    userService
      .createUser(newId)
      .then(response => {
        console.log(response)
        dispatch( setSSH(response) )
        userService
        .getUser(response.id)
        .then(response => {
          dispatch( addUser(response) )
        })
      }).catch( error => console.log("couldn't generate a new user"))
      handleClose()

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
            rows={14}
            fullWidth={true}
            value={sshKeys.privateKey}
            variant="outlined"
          />
        </div>
        <Divider light />
        
      </div>
      <div className={classes.btns}> 
        <Button 
          className={classes.genButton} 
          variant="contained"
          onClick={() => setOpen(true)}
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
      <Modal
        open={open}
        className={classes.modal}
        onClose={handleClose}
        aria-labelledby="simple-modal-title"
        aria-describedby="simple-modal-description"
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 1000,
        }}
      >
        <Fade in={open}>
          <div className={classes.paper}>
            
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography variant="body2" gutterBottom>
                Give an ID for the user
                </Typography>
              </Grid>
              <Grid item xs={3}>
                <TextField 
                  value={newId}
                  onChange={(e) => { setNewId(e.target.value) }}
                  />

                <div className={classes.applyButton}>
                  <Button 
                    onClick={() => generateUser()}
                    size="small"
                    variant="outlined"
                    >
                      Apply
                  </Button>
                </div>
              </Grid>
              
            </Grid>
          </div>
        </Fade>
      </Modal>
    </div>
  )
}

export default CreateUser
