const Pool = require('pg').Pool
const pool = new Pool({
  user: 'soccer',
  host: 'localhost',
  database: 'backend',
  password: 'cole',
  port: 5432,
})
const getPlayer = (request, response) => {
  pool.query('SELECT * FROM player ORDER BY matches_played DESC LIMIT 10', (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

const getClubs = (request, response) => {
  pool.query('SELECT * FROM club ORDER BY club_name DESC LIMIT 10', (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

const getPlayerById = (request, response) => {
  const id = request.params.id

  pool.query('SELECT * FROM player WHERE player_id = $1', [id], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

const getPlayerByName = (request, response) => {
  const id = request.params.id + '%'

  pool.query('SELECT * FROM player WHERE player_name ILIKE $1 ORDER BY matches_played DESC LIMIT 10' , [id], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

const getClubById = (request, response) => {
  const id = request.params.id
  

  pool.query('SELECT * FROM club WHERE club_id = $1', [id], (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

// const createUser = (request, response) => {
//   const { name, email } = request.body

//   pool.query('INSERT INTO users (name, email) VALUES ($1, $2)', [name, email], (error, results) => {
//     if (error) {
//       throw error
//     }
//     response.status(201).send(`User added with ID: ${results.insertId}`)
//   })
// }

// const updateUser = (request, response) => {
//   const id = parseInt(request.params.id)
//   const { name, email } = request.body

//   pool.query(
//     'UPDATE users SET name = $1, email = $2 WHERE id = $3',
//     [name, email, id],
//     (error, results) => {
//       if (error) {
//         throw error
//       }
//       response.status(200).send(`User modified with ID: ${id}`)
//     }
//   )
// }

// const deleteUser = (request, response) => {
//   const id = parseInt(request.params.id)

//   pool.query('DELETE FROM users WHERE id = $1', [id], (error, results) => {
//     if (error) {
//       throw error
//     }
//     response.status(200).send(`User deleted with ID: ${id}`)
//   })
// }

module.exports = {
  getPlayer,
  getClubs,
  getPlayerById,
  getPlayerByName,
  getClubById
  //createUser,
  //updateUser,
  //deleteUser,
}