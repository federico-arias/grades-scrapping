CREATE UNIQUE INDEX dimfecha_index ON dimfecha USING BTREE
	(semestre, ano);

CREATE UNIQUE INDEX dimalumno_index ON dimalumno USING BTREE
	(run);
