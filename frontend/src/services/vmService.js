import axios from 'axios'

const url = 'http://localhost:5000/api/vms/'

const getVMs = async () => {
  const response = await axios.get(`${url}`)
  return response.data
}

export default {
  getVMs
}
