Rotmantic a simple dating application built using Flask and SQLite Cloud. 
The application allows users to create profiles, search for potential matches based on various criteria, and interact with other users by liking or disliking their profiles. 
## Features
- **User Authentication**: Users can log in and out of the application securely.
- **Profile Creation**: New users can create a profile by providing their personal details, interests, and language preferences.
- **Profile Editing**: Users can update their profile information anytime.
- **Profile Deletion**: Users can delete their profile, which removes their data from the database.
- **Matching Algorithm**: Users can find potential matches based on gender preference, location, age difference, interests, and languages.
- **Like Function**: Users can like other profiles, and matches are formed when both users like each other.
- **Dislike Function**: Users can dislike other profiles.

## Steps
1. git clone https://github.com/yourusername/dating-app.git
2. Install the required packages
3. Set up SQLite Cloud database
4. Run the application:python app.py
5. Open your browser and navigate to http://127.0.0.1:5000/ to access the application

## Database Schema
The application uses two main tables:

## User Table

- **UserID**: Unique identifier for the user.
- **password**: User's password.
- **name**: User's name.
- **age**: User's age.
- **gender**: User's gender.
- **gender_preference**: User's gender preference for matches.
- **location**: User's city.
- **interests**: Comma-separated list of user's interests.
- **language(s)**: Comma-separated list of languages the user speaks.

## Records Table

- **UserA**: The ID of the user initiating the action.
- **UserB**: The ID of the user receiving the action.
- **Match**: Whether the two users have matched (1 for yes, 0 for no).
- **Liked**: Whether UserA liked UserB (1 for yes, 0 for no).
- **Disliked**: Whether UserA disliked UserB (1 for yes, 0 for no).
