CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    answer TEXT,
    user_id INTEGER REFERENCES users,
    test_id INTEGER REFERENCES choices,
    
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question TEXT,
    user_id INTEGER REFERENCES tests
    
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    choice TEXT,
    user_id INTEGER REFERENCES tests
    
);

CREATE TABLE tests (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    created_at TIMESTAMP
);

