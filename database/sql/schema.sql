BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS Usuario (
	usuario_id	TEXT,
	nome_usuario	VARCHAR(30) NOT NULL,
	senha	VARCHAR(50) NOT NULL,
	data_criacao TEXT NOT NULL,
	PRIMARY KEY(usuario_id)
);

CREATE TABLE IF NOT EXISTS Post (
	post_id	TEXT,
	titulo	VARCHAR(50) NOT NULL,
	descricao	VARCHAR(255) NOT NULL,
	data_criacao TEXT NOT NULL,
	usuario_id TEXT,
	bloqueado	INTEGER(1) NOT NULL DEFAULT (0),
	FOREIGN KEY(usuario_id) REFERENCES Usuario(usuario_id),
	PRIMARY KEY(post_id)
);

CREATE TABLE IF NOT EXISTS Resposta (
	resposta_id TEXT NOT NULL,
	post_id TEXT NOT NULL,
	descricao  VARCHAR(255) NOT NULL,
	usuario_id TEXT,
	data_criacao TEXT NOT NULL,
	bloqueado	INTEGER(1) NOT NULL DEFAULT (0),
	PRIMARY KEY(resposta_id),
	FOREIGN KEY(post_id) REFERENCES Post(post_id),
	FOREIGN KEY(usuario_id) REFERENCES Usuario(usuario_id)
);

CREATE TABLE IF NOT EXISTS Tag (
	nome VARCHAR(15) NOT NULL,
	data_criacao TEXT NOT NULL,
	PRIMARY KEY(nome)
);


COMMIT;