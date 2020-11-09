import axios from 'axios'

const url = 'http://localhost:5000/api/ports/'

const getPortForwarded = async (id) => {
  const response = await axios.get(`${url}${id}`)
  return response.data
}

export default {
  getPortForwarded
}
