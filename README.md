# ScreenClash
#### Video Demo:  <https://www.youtube.com/watch?v=FaWrJxWUmcw>
#### Description:

Story behind ScreenClash (Project 1A):
I’ve always loved movies, TV shows, and similar content. A long time ago, I watched a movie where the main character created an application that let users compare photos of two people, but they could only like one. That sparked an idea: what if, instead of comparing photos of people, we compared movies or TV shows? I wanted to build an application that did exactly that, but at the time, I didn’t know how. After finishing this course, now I know.
So I made a web application which compares two TV shows. You can create matchups, like them, comment on them, and search for any show that exists. I used Python's Flask for this and of course Python, which blends all my HTML, CSS, JavaScript, and SQL together, to create a beautiful thing and called it "ScreenClash".

Instruction on how to use ScreenClash:

1. On the upper right corner, click register, and register yourself by submitting username and password.

2. On the upper right corner, click login, and then login by typing username and password.

3. In the "search TV show" search box on the upper left corner, type a TV show's name you want details about and click search.

4. A list of TV shows would have appeared on the page; select the one you were looking for.

5. Click "know more" if you want to know more or select the "Add to clash" button if you want to create a matchup. For creating a matchup, you need two shows, so do the same procedure one more time and add another show.

6. A new matchup would have been added to the home page as newly added matchups appear on the top of the list of matchups.

7. You can like any one of the TV shows from each matchup by clicking the like icon (button) which is located just below the TV show.

8. You can comment on any matchup and share your opinion on the comparison by clicking the comment icon which is located between each matchup, below the sword symbol. You can also see other people's opinions on the matchup and discuss with them.

Features:

1. Register - Basic feature of any web application is register. In this, I just implemented the same methods learned in CS50's problem set 9. We take username, password, and confirm password as input from the user via a form. On submitting, the data gets stored in a SQL database table called "users". Used "werkzeug.security" for generating cryptic passwords to be extra safe.

2. Login - Takes input username and password from the user via a form and then checks if the user is valid or not (if the user is present in the users table or not).

3. Search - Given a TV show's name as input, this feature searches and returns all TV shows with that name. I used TMDb's API, which was the best tool I found while working on this project. This API takes a string as input and returns all TV shows (along with their details) that either have the same string in their title or in one of their alternate titles, all formatted as JSON. The result is then passed to the HTML page to display the results.

4. Details - In this route (e.g., /details/1396), each TV show has a unique tmdb_id. '1396' is the tmdb_id for 'Breaking Bad'. By using this route, you can get the details of any (existing) show you searched. Details contain an HTML page displaying the show's runtime, IMDb rating, stars, etc. Used TMDb's API for this as well (once again thanks to TMDb) and also used OMDb's API for the things I didn't get on TMDb's API like genre. Combining this and passing them to the HTML page was the next step. At the bottom of this page, there is a button called "Add to clash"; by clicking this button you can make your own matchup which will then be added to the index page. You need to do this twice though, as there must be two shows to compare. Also adds each TV show users add to clash to the project's own database table called "shows".

5. Matchup - By clicking on the comment icon from any one of the matchups, you will be redirected to /matchup/{matchup_id} where you can comment (fight for your favorite show against the dark forces, just kidding). Keeping a note of every matchup in a database table called "matchups".

6. Index - The index page contains all the matchups created by all the users, showing one matchup in a row, their 'Poster', 'Name', and likes. You can like them, comment on them.

7. Likes - You can like any one show from a matchup. By clicking the like button, a route is called /post/{matchup_id}/{like1 or like2} which then adds your like to a database table called "votes".

8. Comment - You can comment on any available matchup you want. Comments are stored in a database table called "comments" along with their time. The HTML page displays all the comments, with the upper ones being the recent ones. Each comment has username, comment, and the time ago the user commented.

9. Logout - This button logs the user out, clearing their session.

10. Profile - This page will display all the data about the user like username, email they have added, option to change password, their list of shows (will add this feature and let you know), the matchups they have added, etc. Working on "Profile" right now so this one is "Under Construction".

11. GTF - Stay tuned for this feature; its full form is "Guess the Frame" by the way. This one is also "Under Construction".

Files:

1. app.py - Contains all the Python code, uses Flask to run the application.

2. helpers.py - Some helper functions like search_for_tv_show and all the other API calls go through here.

3. static - This folder contains style.css (which has all the CSS properties used by the webpages) and main.js (which contains JavaScript code for the like feature) files, which are then used by the webpages.

4. templates - All the HTML webpages are stored in this folder like layout.html (has code for a common layout which is used by all the other webpages), login.html, register.html, searched.html, details.html, matchup.html, index.html, etc.

5. README.md - This file stores the details about this project "ScreenClash", story behind the idea, working of each feature and file, and instructions on how to use it.

Conclusion:
This project was an incredibly fun and rewarding experience for me. Over the span of just two weeks, I learned many things that I couldn't have gained from simply solving problem sets. I plan to continue improving the application by adding new features, enhancing existing ones, and updating it every month.

