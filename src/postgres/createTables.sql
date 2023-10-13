CREATE TABLE users (
	id SERIAL,
	email TEXT PRIMARY KEY,
	pass TEXT,
	salt TEXT,
	last_login TIMESTAMP
);