"""
Migration script to alter the 'bio' column in the 'profiles' table to TEXT.
"""
ALTER TABLE profiles MODIFY bio TEXT;
