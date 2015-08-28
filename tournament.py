#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")
    
    
def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM Matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM Players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) AS num_players FROM Players;")
    count = c.fetchone()[0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Players (player_name, wins, matches) VALUES (%s, 0, 0)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM Players ORDER BY wins DESC;")
    records = c.fetchall()
    conn.close()
    return records
    


def reportMatch(winner, loser, draw):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw: boolean value, True if there was a draws
    """
    if draw == False:
      conn = connect()
      c = conn.cursor()
      c.execute('''
      INSERT INTO Matches (match_victor, participant_1, participant_2) VALUES (%s, %s, %s)
      ''', (winner, winner, loser))
      c.execute('''
      update Players set (wins, matches) = (wins+1, matches+1)
        where Player_id = %s
      ''' , (winner,))
      c.execute('''
      update Players set (matches) = (matches+1)
        where player_id = %s
      ''' , (loser,))
      conn.commit()
      conn.close()
    elif draw == True:
      conn = connect()
      c = conn.cursor()
      c.execute('''
      INSERT INTO Matches (match_victor, participant_1, participant_2) VALUES (null, %s, %s)
      ''', (winner, loser))
      c.execute('''
      update Players set (matches) = (matches + 1)
        where player_id = %s
      ''' , (winner,))
      c.execute('''
      update Players set (matches) = (matches +1)
        where player_id = %s
      ''' , (loser,))
      conn.commit()
      conn.close()
    else:
      raise TypeError("Please enter a boolean for arg 'draw.'")
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    query = '''
    SELECT e.player_id, e.player_name, o.player_id, o.player_name
    FROM vRankEvens as e, vRankOdds as o
    WHERE e.ranking = o.ranking + 1;
    '''
    c.execute(query)
    pairings = [(row[0], row[1], row[2], row[3]) for row in c.fetchall()]
    
    return pairings


