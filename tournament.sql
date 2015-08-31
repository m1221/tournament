-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Make a new database and connect to it
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament;

-- TABLES --
CREATE TABLE Tournaments (
  tournament_id serial PRIMARY KEY,
  tournament_name text,
  tournament_start date,
  tournament_end date
);

CREATE TABLE Players (
  tournament_id int REFERENCES Tournaments(tournament_id),
  player_id serial PRIMARY KEY,
  player_name text,
  wins int,
  matches int
);

CREATE TABLE Matches (
  match_id serial PRIMARY KEY,
  tournament_id int REFERENCES Tournaments(tournament_id),
  match_victor int REFERENCES Players(player_id),
  participant_1 int REFERENCES Players(player_id),
  participant_2 int REFERENCES Players(player_id)
);

-- VIEWS --
-- These views are used for swissPairings() in tournament.py
CREATE VIEW vRank as
  SELECT player_id, player_name,
    ROW_NUMBER() OVER(ORDER BY wins) AS ranking
  FROM Players;
  
CREATE VIEW vRankOdds AS
  SELECT player_id, player_name, ranking
  FROM vRank
  WHERE ranking % 2 = 1;
  
CREATE VIEW vRankEvens AS
  SELECT player_id, player_name, ranking
  FROM vRank
  WHERE ranking % 2 = 0;