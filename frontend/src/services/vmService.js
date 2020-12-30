import axios from 'axios'

const url = 'http://localhost:5000/api/vms/'

export const getVMs = async () => {
  const response = await axios.get(`${url}`)
  return response.data
}

export const removeUser = async (id) => {
  const response = await axios.put(`${url}${id}`)
  return response.data
}
