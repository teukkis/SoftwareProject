import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'

import vm from './redux/vm'
import user from './redux/user'
import ssh from './redux/ssh'


const rootReducer = combineReducers({
  vmReducer: vm.vmReducer,
  userReducer: user.userReducer,
  sshReducer: ssh.sshReducer
})

const store = createStore(
  rootReducer,
  composeWithDevTools(applyMiddleware(thunk))
)

export default store
