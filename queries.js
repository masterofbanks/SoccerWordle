const Pool = require('pg').Pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

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

const getRandomPlayer = (request, response) => {
  

  pool.query('SELECT player_id FROM player WHERE (current_club = \'822bd0ba\' OR current_club = \'18bb7c10\' OR current_club = \'b8fd03ef\' OR current_club = \'cff3d9bb\' OR current_club = \'19538871\' OR current_club = \'361ca564\' OR current_club = \'b2b47a98\' OR current_club = \'8602292d\' OR current_club = \'d48ad4ff\' OR current_club = \'d609edc0\' OR current_club = \'e0652b02\' OR current_club = \'dc56fe14\' OR current_club = \'cf74a709\' OR current_club = \'206d90db\' OR current_club = \'53a2f082\' OR current_club = \'db3b9613\' OR current_club = \'e2d8892c\' OR current_club = \'054efa67\' OR current_club = \'c7a9f859\' OR current_club = \'add600ae\') AND matches_played > 30;' 
    ,(error, results) => {
    if (error) {
      throw error
    }

    let rnd = Math.floor(Math.random() * results.rows.length);
    response.status(200).json(results.rows[rnd])
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
    name_comparison: compareStrings(player_one.player_name, player_two.player_name),
    positions_comparison: compareSets(player_one.positions, player_two.positions),
    foot_comparison: compareStrings(player_one.foot, player_two.foot),
    height_comparison: compareIntegers(player_one.height, player_two.height),
    age_comparison: compareIntegers(player_one.age, player_two.age),
    nation_comparison: compareStrings(player_one.nationality, player_two.nationality),
    cc_comparison: compareStrings(player_one.current_club, player_two.current_club),
    goals_comparison: compareIntegers(player_one.goals, player_two.goals),
    assists_comparison: compareIntegers(player_one.assists, player_two.assists),
    mp_comparison: compareIntegers(player_one.matches_played, player_two.matches_played),
    league_comparison: compareStrings(player_one.league, player_two.league),
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
  let set_a = new Set(a.split(' '))
  let set_b = new Set(b.split(' '))
  if (set_a.isSubsetOf(set_b) && set_b.isSubsetOf(set_a)) return "equal"
  for(let v of set_a){
    if(set_b.has(v)) return "partial"
  }

  return "no_match"
  
}



module.exports = {
  getPlayer,
  getClubs,
  getPlayerById,
  getPlayerByName,
  getClubById,
  getAllClubs,
  compare,
  getRandomPlayer
  //createUser,
  //updateUser,
  //deleteUser,
}