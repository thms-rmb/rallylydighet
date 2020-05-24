DROP TABLE IF EXISTS sign;
DROP TABLE IF EXISTS sequence;
DROP TABLE IF EXISTS sequence_sign;

CREATE TABLE sign (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    mime TEXT NOT NULL,
    size INTEGER NOT NULL,
    content BLOB NOT NULL
);

CREATE TABLE sequence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sequence_sign (
    sequence_id INTEGER NOT NULL,
    sign_id INTEGER NOT NULL,
    priority INTEGER NOT NULL,
    PRIMARY KEY (sequence_id, sign_id, priority),
    FOREIGN KEY (sequence_id) REFERENCES sequence (id),
    FOREIGN KEY (sign_id) REFERENCES sign (id)
);
