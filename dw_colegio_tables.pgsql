CREATE TYPE financiamiento AS ENUM('privado', 'particular', 'subvencionado');

CREATE TABLE IF NOT EXISTS DimProfesor (
	id serial,
	nombre 		varchar(100),
	apellido 	varchar(255),

	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS DimFecha (
	id serial,
	semestre smallint,
	ano integer,
	
	PRIMARY KEY (id)
	);

CREATE TABLE IF NOT EXISTS DimColegio (
	id serial,
	nombre varchar,
	ubicacion varchar,
	financiamiento financiamiento,

	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS DimAsignatura (
	id serial,
	nombre varchar(80),

	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS DimAlumno (
	id serial,
	run integer,
	nombres varchar,
	apellido varchar(39),
	edad integer,

	PRIMARY KEY (id)
);

/*
CREATE TABLE IF NOT EXISTS DimEscala (
	id integer,
	notaMax integer,
	notaMin integer,

	PRIMARY KEY(id)
	);
*/

CREATE TABLE IF NOT EXISTS FactNotas (
	id 				serial,
	nota			decimal(3,2),
	profesorId		integer,
   	fechaId			integer,
	colegioId		integer,
	asignaturaId	integer,
	alumnoId		integer,

	CHECK(nota >=0),
	CHECK(nota <= 7),
	PRIMARY KEY (id),
	FOREIGN KEY (profesorId) REFERENCES DimProfesor(id),
	FOREIGN KEY (fechaId) REFERENCES DimFecha(id),
	FOREIGN KEY (colegioId) REFERENCES DimColegio(id),
	FOREIGN KEY (asignaturaId) REFERENCES DimAsignatura(id),
	FOREIGN KEY (alumnoId) REFERENCES DimAlumno(id)
);
