# README.md file for Udacity Fullstack Nanodegree Tournament Project
Student: Mario P.
Student OS: Windows 8.1
GitHub: m1221

## File log for Tournament:
1. README.md
1. tournament.py
1. tournament.sql
1. tournament_test.py

## Instructions for running:
1. In GitBash, cd to Udacity prepared Vagrant directory
1. Launch VM by VirtualBox configured with Vagrant
  `$vagrant up`
1. Log into the VM
  `$vagrant ssh`
1. cd to tournament directory
1. `$ psql`
1. Enter \i connect tournament.sql
1. Quit by entering \q
1. To test the database, $ python tournament_test.py

# This code has the following extra credit functionality:
1. players can draw
1. database schema supports multiple tournaments