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
    c.execute("UPDATE players SET matches = 0;")
    c.execute("UPDATE players SET wins = 0;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) AS total_players FROM players;")
    result = c.fetchone()[0]
    return int(result)

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    name = name.replace('"', "'")
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name, wins, matches) VALUES (%s, %s, %s)", (name, 0, 0))
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
    c.execute("SELECT id, name, wins, matches FROM players ORDER BY wins DESC;")
    result = c.fetchall()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser))

    # Update Winner's Matches
    c.execute("SELECT players.matches FROM players WHERE players.id = %s", (winner,))
    winner_matches = int(c.fetchone()[0]) + 1
    c.execute("UPDATE players SET matches = %s WHERE id = %s", (winner_matches, winner))

    # Update Loser's Matches
    c.execute("SELECT players.matches FROM players WHERE players.id = %s", (loser,))
    loser_matches = int(c.fetchone()[0]) + 1
    c.execute("UPDATE players SET matches = %s WHERE id = %s", (loser_matches, loser))

    # Update Winner's Wins
    c.execute("SELECT players.wins FROM players WHERE players.id = %s", (winner,))
    winner_wins = int(c.fetchone()[0]) + 1
    c.execute("UPDATE players SET wins = %s WHERE id = %s", (winner_wins, winner))

    conn.commit()
    conn.close()
 
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

    pairs_list = playerStandings()
    list_list = []

    for pair in pairs_list:
        list_list.append(list(pair))

    i = 0
    j = len(pairs_list)

    while (i < j):
        list_list[i] = list_list[i] + list_list[i+1]
        del list_list[i][2]
        del list_list[i][2]
        del list_list[i][4]
        del list_list[i][4]

        del list_list[i+1]
        i  = i + 1
        j = j - 1

    tuples_list = []
    for l in list_list:
        tuples_list.append(tuple(l))

    return tuples_list


