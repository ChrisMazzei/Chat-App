Creating a Chat App

Note: Instructions assume you are using AWS Cloud9.
      Cloning repo refers to the original projects repo, which is in a private repo. Access may be available upon request.

# Setup the Translator
1. Start off small by running the command `pip install translate`

# Setup React
1. Run the command `cd ~/environment && git clone https://github.com/NJIT-CS490/project2-m1-cm544` in your terminal.
2. Install the following:
  a) `npm install`    
  b) `pip install flask-socketio`    
  c) `pip install eventlet`    
  d) `npm install -g webpack`    
  e) `npm install --save-dev webpack`    
  f) `npm install socket.io-client --save`    
  g) NOTE: If any errors occur use `sudo pip` or `sudo npm`. If the error is 'pip cannot be found', run the command `which pip`,
           and use `sudo [path that which pip returns] install`

# Installs needed before setting up PSQL
1. Update yum: `sudo yum update`, and enter yes to all prompts    
2. Upgrade pip: `sudo /usr/local/bin/pip install --upgrade pip`  
3. Get psycopg2: `sudo /usr/local/bin/pip install psycopg2-binary`    
4. Get SQLAlchemy: `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`  

# Setting up PSQL
1. Install PostGreSQL with the command `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`
2. Initialize PSQL database with the command `sudo service postgresql initdb`
3. Start PSQL with the command `sudo service postgresql start`
   NOTE: step 4 and 5 may result in an error stating 'could not change directory', ignore this error, it worked.
4. Create a new superuser: `sudo -u postgres createuser --superuser $USER`
5. Create a new database: `sudo -u postgres createdb $USER`
6. Verify your user and datbase shows up with the following commands.
   a) `psql`
   b) `\du`
   c) `l`
   Note: exit psql with `\q`
7. If you exited psql re-enter with `psql`
8. Create a new user with the command `create user [some_username_here] superuser password '[some_unique_new_password_here]';`
9. Exit psql with `\q`
10. Change directorys to `project2-m1-cm544` and make a new file called `sql.env` and add `DATABASE_URL=postgresql://username:password@localhost/postgres`
11. Replace the username and password with the username and password you used in step 8.
    NOTE: Future logins may require `psql -U username -d postgres`, followed by a prompt asking for password
12. *IMPORTANT* Now run the command `c9 open .gitignore` and write to the file `sql.env`. This will ignore the `sql.env` file when pushing your code to github.

# Enabling read/write from SQLAlchemy
To enable the username and password from the Setting up PSQL section we need to do the following steps:
1. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf` If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`
2. Replace all values of ident with md5 in Vim: :%s/ident/md5/g
3. After changing those lines, run sudo service postgresql restart

# Running the application
To run the application open 3 seperate terminals and change directorys in each of them to `project2-m1-cm544`
These terminal tabs will be refered to as A, B, and C.
1. In terminal A run the command `sudo service postgresql start`
2. In terminal B run the command `npm run watch`. If this is your first time running the command you will be prompted to install the webpack, type `yes`
3. In terminal C run the command `python app.py`
4. Now you can view your application in the Preview Running Application tab.

# Sign up for and Install Heroku
1. Create a Heroku account here: https://id.heroku.com/login
2. Run the command `npm install -g heroku` in the terminal to install Heroku
3. Verify the install with the command `heroku --version`, if errors occur debug with this source: https://devcenter.heroku.com/articles/heroku-cli#uninstalling-the-legacy-heroku-gem
4. Login to heroku through the terminal with the command `heroku login`, if errors occur use `heroku login -i`

# Deploy to Heroku
1. Change directorys to `project2-m1-cm544`
2. Login to Heroku with the command `heroku login -i`
3. Create project with the command `heroku create`
4. Make a new database with `heroku addons:create heroku-postgresql:hobby-dev`
5. Run the command `heroku pg:wait`
6. Open your psql with `psql` (login if needed, refer to Notes: in the "Setting up PSQL" section)
7. Run the command `ALTER DATABASE Postgres OWNER TO [name];`
8. Run the command `\l` to verify the postgres table has an owner of [name]
9. Exit psql with `\q` and run the command `PGUSER=[name] heroku pg:push postgres DATABASE URL`, enter password when prompted to
10. Run the command `heroku pg:psql` to push the database
11. Exit psql with `\q`
12. Create a requirements.txt file with the command `pip freeze > requirements.txt`
    Note: pip freeze is not always reccomended but in this case it is done for simplicity.
          pip freeze will add all installed packages to the requirements.txt file.
13. Use the commands `git add requirements.txt`, `git commit -m "[message]"`, and `git push origin main` to add, commit and push your requirements.txt to github
14. Push to heroku with the command `git push heroku main`
15. Debug with the command `heroku logs --tail` if needed

# Known Problems:
1. Currently no known problems.

# Common Issues:
1. Refer to `Notes` in the Section you are experiencing issues with.

# Future Improvements:
1. Currently the app does not display to total amount of users connected.
   Ran out of time trying to implement this in a varity of different ways.
   If I had more time I would try to keep track of users signed in through the database by adding and removing users 
   that connect and disconnect from the socket.
2. No external API is used.
   I think a fun API to use would be a Google searcher implemented into a bot with the command `!! google [whatever you want to search]`
   Since the Google Custom Search API returns JSON code I would parse it for the first link and the chat bot would respond in the chat with that link.
   This would be the same concept of the "I'm feeling lucky" button.
3. Create an account. 
   Currently the web app only allows a nickname for users, which is kinda cool because users can easily change it.
   A downside to users being able to change their name whenever is that people are practically anonymous. 
   I should have made a database that stored usernames and passwords so I could add a login feature.

Issues I Encountered:
1. The first issue I encountered was when running the project in the web browser it was working but,
   in the Cloud9 terminal I kept getting errors and my program would not display in the preview running application window.
   It turned out that hard refreshing was only working in the other browser window and not in Cloud 9 window.
   I resulted to seeking help in the slack general chat, turns out I just had to disable the cache in Cloud9's preview application window.
2. Another issue I encountered was my css code not working when I had it written in a .css file in `/templates`. I spent alot of time on this and ended up taking the easy way out of
   writing the css code directly in the jsx files. Prior to that I did a lot of reading on stackoverflow and messing around in the 
   `webpack.config.js` file but, no luck. I should have brought it up in the slack chat but I was just stuck in the googling loop and wasted to much time on it. So I just wrote the css in 
   the jsx files directly.
3. I also encountered an issue when deploying my project to Heroku. Although I did not document the exact errors I do remember the cause.
   I was able to debug my issue by rewatching the `Lecture 11 Demo 3` video on YouTube. Turns out, when leaving `sql_[user/pass] = os.environ[SQL_USER]` in app.py
   after adding the `datbase_uri` to the `sql.env` and `app.py`, the heroku deployment doesnt respond to well.
