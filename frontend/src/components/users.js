import React, {useState, useEffect} from 'react';
import { useSelector, useDispatch } from 'react-redux'

import { DataGrid } from '@material-ui/data-grid';
import Modal from '@material-ui/core/Modal';
import { makeStyles } from '@material-ui/core/styles';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';

import userService from '../services/userService'
import portService from '../services/portService'
import { setSSH } from '../redux/ssh'
import { setUsers, deleteUser } from '../redux/user'


const columns = [
  {
    field: "id",
    headerName: "user ID",
    width: 320
  },
  {
    field: "status",
    headerName: "Status",
    width: 100
  },
]

const useStyles = makeStyles((theme) => ({
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
    width: 700,
  },
  actions: {
    display: 'inline'
  },
  deleteButton: {
    marginTop: 8
  },
  refreshButton: {
    marginLeft: 15,
    marginTop: 10,
  },
  dataGrid: {
    height: 620, 
    width: '95%',
    marginLeft: 14,
    paddingTop: 10
  }
}));

const Users = () => {

  const classes = useStyles()

  const [ activeInfo, setActiveInfo ] = useState('')
  const [ open, setOpen ] = useState(false)

  const users = useSelector( state => state.userReducer)
  const dispatch = useDispatch()

  const handleClose = () => {
    setOpen(false);
  };

  const handleRowClick = (event) => {
    setActiveInfo(event.data.id)
    setOpen(true)
  }

  const deleteWorkspace = async () => {
    await userService.deleteUser(activeInfo)
    dispatch( deleteUser(activeInfo) )

    setActiveInfo('')
    handleClose()
  }

  const diveIntoWorkspace = async () => {
    const response = await portService.getPortForwarded(activeInfo)
    console.log(response)
    setActiveInfo('')
    handleClose()
  }

  const createNewSSHPair = async () => {
    const response = await userService.editUser(activeInfo)
    dispatch( setSSH(response) )
    setActiveInfo('')
    handleClose()
  }

  const getUsers = () => {
    userService
      .getUsers()
      .then(response => {
        dispatch( setUsers(response) )
      }).catch( error => console.log("couldn't retrieve users"))
  }

  useEffect( () => {
    getUsers()
  }, [])

  return (
    <div>
       <div className={classes.dataGrid}>
        <DataGrid 
          rows={users.users} 
          columns={columns}
          hideFooter={true}
          onRowClick={handleRowClick}
          checkboxSelection={false}
          />
      </div>
      <Button 
        className={classes.refreshButton} 
        variant="contained"
        onClick={() => getUsers()}
        >
          Refresh users
      </Button>

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
                  Available actions for user: {activeInfo}
                </Typography>
              </Grid>
              <Grid item xs={3}>
                <Typography variant="caption" gutterBottom>
                  Delete the workspace
                </Typography>
                <div className={classes.deleteButton}>
                  <Button 
                    className={classes.button} 
                    onClick={() => deleteWorkspace()}
                    size="small"
                    variant="outlined"
                    >
                      Delete
                  </Button>
                </div>
              </Grid>
              <Divider orientation="vertical" flexItem/>
              <Grid item xs={4}>
                <Typography variant="caption" gutterBottom>
                  Maybe diving into the workspace...
                </Typography>
                <div className={classes.deleteButton}>
                  <Button 
                    className={classes.button} 
                    onClick={() => diveIntoWorkspace()}
                    size="small"
                    variant="outlined"
                    >
                      Dive
                  </Button>
                </div>
              </Grid>
              <Divider orientation="vertical" flexItem/>
              <Grid item xs={4}>
                <Typography variant="caption" gutterBottom>
                  Create a new ssh key pair for the user
                </Typography>
                <div className={classes.deleteButton}>
                  <Button 
                    className={classes.button} 
                    onClick={() => createNewSSHPair()}
                    size="small"
                    variant="outlined"
                    >
                      Create
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

export default Users
