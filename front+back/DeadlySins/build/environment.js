const os = require('os')

const configArgv = JSON.parse(process.env.npm_config_argv)
const original = configArgv.original.slice(1)
const stage = original[1] ? original[1].replace(/-/g, '') : ''

let localUrl
try {
  const network = os.networkInterfaces()
  localUrl = network[Object.keys(network)[0]][1].address
} catch (e) {
  localUrl = 'localhost'
}
localUrl = 'http://' + localUrl + ':5000/'

module.exports = {
  stage, localUrl
}
