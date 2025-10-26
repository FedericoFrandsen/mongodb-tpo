// 1) Constraints (unicidad)
CREATE CONSTRAINT persona_id IF NOT EXISTS
FOR (p:Persona) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT empresa_id IF NOT EXISTS
FOR (e:Empresa) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT oferta_id IF NOT EXISTS
FOR (o:Oferta) REQUIRE o.id IS UNIQUE;
CREATE CONSTRAINT curso_id IF NOT EXISTS
FOR (c:Curso) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT skill_nombre IF NOT EXISTS
FOR (s:Skill) REQUIRE s.nombre IS UNIQUE;
CREATE CONSTRAINT interes_nombre IF NOT EXISTS
FOR (i:Interes) REQUIRE i.nombre IS UNIQUE;

// 2) nodos y relaciones
MERGE (ana:Persona {id: "cand-ana"}) SET ana.nombre="Ana Torres", ana.tipo="candidato";
MERGE (luis:Persona {id: "cand-luis"}) SET luis.nombre="Luis García", luis.tipo="candidato";

MERGE (tal:Empresa {id:"emp-talentum"}) SET tal.nombre="Talentum+";
MERGE (of1:Oferta {id:"of-backend"}) SET of1.puesto="Backend Node.js";
MERGE (of1)-[:DE_EMPRESA]->(tal);

MERGE (skNode:Skill {nombre:"Node.js"});
MERGE (skMongo:Skill {nombre:"MongoDB"});
MERGE (of1)-[:REQUIERE {nivel: 6}]->(skNode);
MERGE (of1)-[:REQUIERE {nivel: 5}]->(skMongo);

MERGE (ana)-[:TIENE_SKILL {nivel: 7}]->(skNode);
MERGE (ana)-[:TIENE_SKILL {nivel: 6}]->(skMongo);
MERGE (luis)-[:TIENE_SKILL {nivel: 5}]->(skNode);
MERGE (luis)-[:TIENE_SKILL {nivel: 4}]->(skMongo);

MERGE (ana)-[:POSTULO {fecha: date(), estado:"en_proceso"}]->(of1);
MERGE (luis)-[:POSTULO {fecha: date(), estado:"aplicado"}]->(of1);

MERGE (ana)-[:CONOCE {desde: date("2024-01-01"), peso: 0.8}]->(luis);

MERGE (c1:Curso {id:"c-mongodb"}) SET c1.titulo="MongoDB Básico";
MERGE (ana)-[:CURSO_TOMADO {progreso: 60, desde: date("2025-09-20")}]->(c1);
MERGE (luis)-[:CURSO_TOMADO {progreso: 20, desde: date("2025-10-01")}]->(c1);

MERGE (intNoSql:Interes {nombre:"NoSQL"});
MERGE (ana)-[:INTERES_EN]->(intNoSql);
MERGE (luis)-[:INTERES_EN]->(intNoSql);

// 3) Verificación simple
MATCH (n) RETURN count(n) AS total_nodos;