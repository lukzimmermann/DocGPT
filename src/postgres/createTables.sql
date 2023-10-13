CREATE TABLE users (
	id SERIAL,
	email TEXT PRIMARY KEY,
	password_hash TEXT,
	last_login TIMESTAMP
);