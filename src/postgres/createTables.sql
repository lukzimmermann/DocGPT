CREATE TABLE users (
	id SERIAL,
	email TEXT PRIMARY KEY,
	pass TEXT,
	last_login TIMESTAMP,
	is_verified BOOLEAN,
	is_active BOOLEAN,
	is_admin BOOLEAN
);