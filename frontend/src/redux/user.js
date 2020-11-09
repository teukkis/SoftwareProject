const SET_USERS = 'SET_USERS'
const DELETE_USER = 'DELETE_USER'
const ADD_USER = 'ADD_USER'

const initialState = {
  users: [
    
  ]
}

const userReducer = ( state = initialState, action ) => {

  switch ( action.type ) {
    case SET_USERS:
      return { ...state, users: action.payload }

    case DELETE_USER:
      return { users: state.users.filter( u => u.id !== action.payload ) }

    case ADD_USER:
      return { users: state.users.concat(action.payload) }

    default:
      return state
  }
}

export const setUsers = ( users ) => {
  return  {
    type: SET_USERS,
    payload: users
  }
}

export const deleteUser = ( userID ) => {
  return  {
    type: DELETE_USER,
    payload: userID
  }
}

export const addUser = ( user ) => {
  return  {
    type: ADD_USER,
    payload: user
  }
}

export default { userReducer }
