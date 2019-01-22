Nothing working yet.

Fetches the person who is at-bat from Reddit.  Pings them in Discord or on Reddit if they'd prefer.  Or both. 

Eventually will also ping their GM.


------
**Database Setup**

This thing uses a PostgreSQL Database to keep state about who wants to be reminded and how they
want to be pinged.  There's not a good way to do this securely, so I'm gonna walk
you through it.

I **HIGHLY** recommended using a Linux server for this!

1) Run 'sudo apt install postgresql-client-common'
2) Go here: https://websiteforstudents.com/installing-postgresql-10-on-ubuntu-16-04-17-10-18-04/
   -> That website is for Ubuntu but the process is the same for most common
   Linux distros.
3) After the setup for that, create a non-admin user and give it a password.
You're going to use this user in the bot's configuration.
4) Finally, run the command 'CREATE DATABASE mlnbot'

---------
**Configuring the Bot**