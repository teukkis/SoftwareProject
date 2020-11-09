const SET_VMS = 'SET_VMS'

const initialState = {
  vms: []
}

const vmReducer = (state = initialState, action) => {

  switch (action.type) {
    case SET_VMS:
      return { ...state, vms: action.payload }

    default:
      return state
  }
}

export const setVms = (vms) => {
  return  {
    type: SET_VMS,
    payload: vms
  }
}

export default { vmReducer }
