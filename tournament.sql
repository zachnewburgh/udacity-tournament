-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

-- players table
CREATE TABLE players (
  id serial PRIMARY KEY,
  name text NOT NULL
);

-- matches table
CREATE TABLE matches (
  id serial PRIMARY KEY,
  winner integer REFERENCES players (id) ON DELETE CASCADE,
  loser integer REFERENCES players (id) ON DELETE CASCADE
);