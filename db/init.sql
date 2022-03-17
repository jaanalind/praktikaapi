CREATE TABLE elering_data (
	id SERIAL PRIMARY KEY,
    production real,
    consumption real,
	price real,
	ts timestamptz
);