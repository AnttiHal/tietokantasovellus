CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    answer INTEGER
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    choice TEXT
);

