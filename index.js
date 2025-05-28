const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const db = require('./queries')
const port = 3000

app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)

app.get('/', (request, response) => {
  response.json({ info: 'Node.js, Express, and Postgres API' })
})

app.get('/Player', db.getPlayer)
app.get('/random', db.getRandomPlayer)
app.get('/clubs', db.getAllClubs)
app.get('/Player/:id', db.getPlayerById)
app.get('/Player/name/:id', db.getPlayerByName)
app.get('/clubs/:id', db.getClubById)
app.post('/compare', db.compare)
//app.post('/users', db.createUser)
//app.put('/users/:id', db.updateUser)
//app.delete('/users/:id', db.deleteUser)

app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})