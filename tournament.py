#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Delete all entries in the matches table."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE matches CASCADE;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Delete all entries in the players table."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE players CASCADE;")
    conn.commit()
    conn.close()


def countPlayers():
    """Return the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) AS total_players FROM players;")
    result = c.fetchone()[0]
    return int(result)


def registerPlayer(name):
    """Add a player to the tournament database."""
    name = name.replace('"', "'")
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name)"
              "VALUES (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Return a list of player ids, names, wins,
    and matches sorted by wins (highest to lowest)."""
    conn = connect()
    c = conn.cursor()

    # Retrieve a list of winners.
    c.execute("SELECT players.id, name, "
              "COUNT(matches.winner) AS wins, "
              "COUNT(matches.winner) AS matches "
              "FROM players, matches "
              "WHERE players.id = matches.winner "
              "GROUP BY players.id "
              "ORDER BY wins DESC;")
    winners = c.fetchall()

    # Retrieve of list of losers.
    c.execute("SELECT players.id, name, "
              "0 AS wins, "
              "COUNT(matches.loser) AS matches "
              "FROM players, matches "
              "WHERE players.id = matches.loser "
              "GROUP BY players.id;")
    losers = c.fetchall()

    # Retrieve a list of registered players who haven't yet played.
    c.execute("SELECT players.id, name, 0 AS wins, 0 AS matches "
              "FROM players "
              "WHERE NOT EXISTS (SELECT players.id, "
                                "name "
                                "FROM players, matches "
                                "WHERE players.id = matches.winner);")
    unplayed = c.fetchall()

    # Combine the winners, losers, and unplayed queries into a single list.
    result = []
    for winner in winners:
        result.append(winner)
    for loser in losers:
        result.append(loser)
    for player in unplayed:
        result.append(player)

    return result


def reportMatch(winner, loser):
    """Record the outcome of a single match between two players."""
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (winner, loser) "
              "VALUES (%s, %s)", (winner, loser))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Returns:
    A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()

    # Retrieve a list of player tuples sorted by most to least wins.
    pairs_list = playerStandings()

    # Create a new list comprised of pairs_list's tuples coverted into lists.
    list_list = []
    for pair in pairs_list:
        list_list.append(list(pair))

    # Iterate over list_list to create pairs of consecutive lists.
    i = 0
    j = len(list_list)
    while (i < j):
        # Join the current list with the consecutive list.
        list_list[i] = list_list[i] + list_list[i+1]
        # Remove the first player's wins from the current list.
        del list_list[i][2]
        # Remove the first player's matches from the current list.
        del list_list[i][2]
        # Remove the second player's wins from the current list.
        del list_list[i][4]
        # Remove the second player's matches from the current list.
        del list_list[i][4]

        """
        Delete the consecutive list from list_list
        since it was already joined to the previous list."""
        del list_list[i+1]

        # Increment the index.
        i = i + 1
        """Decrement j (list_list's original length)
        since an element has been removed."""
        j = j - 1

    # Create a new list comprised of list_list's lists coverted into tuples.
    tuples_list = []
    for l in list_list:
        tuples_list.append(tuple(l))

    return tuples_list
