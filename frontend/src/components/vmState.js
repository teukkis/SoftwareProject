import React, {useState, useEffect} from 'react';
import { useSelector, useDispatch } from 'react-redux'

import { DataGrid } from '@material-ui/data-grid';
import Modal from '@material-ui/core/Modal';
import { makeStyles } from '@material-ui/core/styles';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Divider from '@material-ui/core/Divider';
import Grid from '@material-ui/core/Grid';

import vmService from '../services/vmService'
import { setVms } from '../redux/vm'


const columns = [
  {
    field: 'id',
    headerName: 'ID',
    width: 180
  },
  {
    field: 'state',
    headerName: 'State',
    width: 180
  },
  {
    field: 'user',
    headerName: 'User',
    width: 320 
  }
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
    width: 400
  },
  actions: {
    display: 'inline'
  },
  refreshButton: {
    marginLeft: 15,
    marginTop: 10,
  },
  dataGrid: {
    height: 200,
    width: '96%',
    marginLeft: 14,
    paddingTop: 10
  }
}));

const VMState = () => {

  const classes = useStyles()

  const [activeInfo, setActiveInfo] = useState('')
  const [open, setOpen] = useState(false);
  const vms = useSelector( state => state.vmReducer)
  const dispatch = useDispatch()

  const handleClose = () => {
    setOpen(false);
  };

  const handleRowClick = (event) => {
    setActiveInfo(event.data.id)
    setOpen(true)
  }

  const shutDownVm = () => {

    setActiveInfo('')
    handleClose()
  }

  const freeVm = () => {

    setActiveInfo('')
    handleClose()
  }

  const refreshVMs = () => {
    vmService
      .getVMs()
      .then(response => {
        dispatch( setVms(response) )
      }).catch( error => console.log("couldn't retrieve vms"))
  }

  useEffect( () => {
    refreshVMs()
  }, [])

  return (
    <div>
      <div className={classes.dataGrid}>
        <DataGrid 
          rows={vms.vms} 
          columns={columns}
          hideFooter={true}
          onRowClick={handleRowClick}
        />
      </div>
      <Button 
        className={classes.refreshButton} 
        variant="contained" 
        onClick={() => refreshVMs()}
        >
          Refresh VMs state
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
                  Available actions for virtual machine {activeInfo}
                </Typography>
              </Grid>
              <Grid item xs={5}>
                <Typography variant="caption" gutterBottom>
                  Delete the workspace
                </Typography>
                <div className={classes.deleteButton}>
                  <Button 
                    className={classes.button} 
                    onClick={() => shutDownVm()}
                    size="small"
                    variant="outlined"
                    >
                      Power off
                  </Button>
                </div>
              </Grid>
              <Divider orientation="vertical" flexItem/>
              <Grid item xs={5}>
                <Typography variant="caption" gutterBottom>
                  Kick out the current user
                </Typography>
                <div className={classes.deleteButton}>
                  <Button 
                    className={classes.button} 
                    onClick={() => freeVm()}
                    size="small"
                    variant="outlined"
                    >
                      Clear
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

export default VMState
