# Tournament

This Python application is a database schema to store the game matches between players in a Swiss-system tournament. 

## Installation

1. Download and install the base [VirtualBox platform package](https://www.virtualbox.org/wiki/Downloads).

2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html).

3. Fork this repo, change into the project's directory, and start up the virtual machine by typing the following into the command line. Note that this could take several minutes.

```
$ vagrant up
```

4. Log into the virtual machine by typing the following into the command line:

```
$ vagrant ssh
```

5. Change to the following directory by typing in the command line:

```
vagrant@vagrant-ubuntu-trusty-32:~$ cd /vagrant/tournament
```

6. Open psql, create the database, connect to the database, import the SQL schema, and run the tests by typing the following in the command line:

```
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql

vagrant=> create database tournament

vagrant=> \c tournament

tournament=> \i tournament.sql

tournament=> \q

vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
```

## License

The application is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).