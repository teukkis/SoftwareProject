const SET_SSH_KEYS = 'SET_SSH_KEYS'
const CLEAR_SSH_KEYS = 'CLEAR_SSH_KEYS'

const initialState = {
  privateKey: '',
  publicKey: ''
}

const sshReducer = (state = initialState, action) => {
  
  switch (action.type) {
    case SET_SSH_KEYS:
      return { 
        ...state, 
        privateKey: action.payload.privateKey,
      }
    case CLEAR_SSH_KEYS:
      return {
        ...state, ...action.payload
      }

    default:
      return state
  }
}

export const setSSH = (keys) => {
  return  {
    type: SET_SSH_KEYS,
    payload: keys
  }
}

export const clearSSH = () => {
  return  {
    type: CLEAR_SSH_KEYS,
    payload: initialState
  }
}

export default { sshReducer }
