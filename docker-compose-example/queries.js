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
  const id = '%' + request.params.id + '%'

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

const getAllClubs = (request, response) => {
  const id = request.params.id
  

  pool.query('SELECT * FROM club', (error, results) => {
    if (error) {
      throw error
    }
    response.status(200).json(results.rows)
  })
}

const compare = async (request, response) => {
  const {id1, id2} = request.body


  const result1 = await pool.query('SELECT * FROM player WHERE player_id = $1', [id1])
  const result2 = await pool.query('SELECT * FROM player WHERE player_id = $1', [id2])
  if (result1.rows.length === 0 || result2.rows.length === 0) {
    return response.status(404).json({ error: 'One or both players not found' })
  }

  const player_one = result1.rows[0]
  const player_two = result2.rows[0]


  const answer = {
    positions_comparison: compareSets(player_one.positions, player_two.positions),
    foot_comparison: compareStrings(player_one.foot, player_two.foot),
    height_comparison: compareIntegers(player_one.height, player_two.height),
    age_comparison: compareIntegers(player_one.age, player_two.age),
    nation_comparison: compareStrings(player_one.nationality, player_two.nationality),
    cc_comparison: compareStrings(player_one.current_club, player_two.current_club),
    goals_comparison: compareIntegers(player_one.goals, player_two.goals),
    assists_comparison: compareIntegers(player_one.assists, player_two.assists),
    mp_comparison: compareIntegers(player_one.matches_played, player_two.matches_played),
    cpf_comparison: compareSets(player_one.clubs_played_for, player_two.clubs_played_for)

  }

  response.json(answer)
}


function compareIntegers(a, b){
  if(a == null || b == null) return "unknown"

  if(a > b) return "greater"
  if(a < b) return "less_than"
  if(a == b) return "equal"
}

function compareStrings(a, b){
  if(a == null || b == null) return "unknown"
  if(a == b) return "equal"
  else return "no_match"
}

function compareSets(a,b){
  let set_a = makeSet(a)
  let set_b = makeSet(b)
  if (set_a === set_b) return "equal"
  for(let v of set_a){
    if(set_b.has(v)) return "partial"
  }

  return "no_match"
  
}

function makeSet(input){
  let x = 0
  let start = 0
  let word = ""
  let answer = new Set()
  for (letter in input){
    if(letter == ' '){
      word = input.substring(start, x)
      answer.add(word)
      start = x + 1
    }

    x = x + 1

  }

  word = input.substring(start, x-1)
  answer.add(word)
  return answer
}

module.exports = {
  getPlayer,
  getClubs,
  getPlayerById,
  getPlayerByName,
  getClubById,
  getAllClubs,
  compare
  //createUser,
  //updateUser,
  //deleteUser,
}