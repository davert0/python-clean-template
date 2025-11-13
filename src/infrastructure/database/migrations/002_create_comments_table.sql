CREATE TABLE if not exists comments (
    post_id serial PRIMARY KEY,
    user_id INTEGER references users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);