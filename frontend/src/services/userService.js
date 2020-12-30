import axios from 'axios'

const url = 'http://localhost:5000/api/users/'

export const getUser = async (id) => {
  const response = await axios.get(`${url}${id}`)
  return response.data
}

const getUsers = async () => {
  const response = await axios.get(`${url}`)
  return response.data
}

const createUser = async (id) => {
  const response = await axios.post(`${url}`, {id: id})
  return response.data
}

const editUser = async (id) => {
  const response = await axios.put(`${url}${id}`, {})
  return response.data
}

const deleteUser = async (id) => {
  const response = await axios.delete(`${url}${id}`)
  return response.data
}

export default {
  getUser,
  getUsers,
  createUser,
  deleteUser,
  editUser
}
