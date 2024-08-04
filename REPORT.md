# Marriage Matchmaking App

## Brief Description
The Marriage Matchmaking App is a simple backend application designed to help users find potential matches based on their profile information. The app allows users to create, read, update, and delete profiles with details such as name, age, gender, email, city, and interests.

## Basic Project Structure:

- **main.py** : The main application file with basic CRUD operations for user profiles.
- **models.py**: SQLAlchemy models defining the User schema.
- **database.py**: Database configuration and setup.
- **schemas.py**: Pydantic schemas for data validation and serialization.

## Assumptions:

- In every user profile, `gender` is either `"male"` or `"female"`.
- All users have ages above the legal marriage age.
- The maximum number of `interests` each user can mention is 10.
- The requirements for a potential match are:
 - Should not be of the same gender.
 - Should be from the same city.
 - Should have at least one mutual interest.
- When a user profile is deleted, all data related to that user should be removed from the database instead of marking as inactive.
- When creating a new user profile, `id` will be provided in the request body.
- When updating a user profile by id, the unchanged fields with their current values will also be provided in the request body along with the changed fields and their updated values.

## Changes made to the existing models:

- In **models.py**, `interests` was originally defined as `Column(ARRAY(String))`. Since we are using SQLite database which does not support arrays, I have defined a new table called *interests* which stores each element of the array as `hobby` in a separate record and also stores the `user_id` of the corresponding user as `foriegn_key` to link to the user profile.
- In `class UserBase` pydantic model, I changed the data type of `email` field from `str` to the pydantic data type `EmailStr` which ensures that its input is a valid email address string.

## Tasks completed:

1. Added `update_user` Endpoint:
   - Implements an endpoint("/users/{user_id}") to update user details by ID in the main.py file.
2. Added `delete_user` Endpoint:
   - Implements an endpoint("/users/{user_id}") to delete a user profile by ID.
3. Added `find_matches` Endpoint:
   - Implements an endpoint("/users/{user_id}") to find potential matches for a user based on their profile information.
4. Added Email Validation:
   - Added validation to ensure the email field in user profiles contains valid email addresses.

## Tests done:

1. Verified that users can be updated and deleted correctly.
2. Checked that matches are correctly retrieved for a given user.
3. Ensured email validation is working as expected.

**Note:** Due to time constraints, I could not implement error handling in the code.