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
    test_id INTEGER REFERENCES tests
    
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    note TEXT,   
    test_id INTEGER REFERENCES tests
    
);


CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    choice TEXT,
    test_id INTEGER REFERENCES tests
    
);

CREATE TABLE tests (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    created_at TIMESTAMP
);

CREATE TABLE audios (
    id SERIAL PRIMARY KEY,
    audio_url TEXT,
    test_id INTEGER REFERENCES tests
);

