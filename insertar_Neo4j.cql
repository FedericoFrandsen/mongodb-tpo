// ===========================
// 1) Constraints de unicidad
// ===========================

CREATE CONSTRAINT candidato_id IF NOT EXISTS
FOR (c:Candidato) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT empresa_id IF NOT EXISTS
FOR (e:Empresa) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT oferta_id IF NOT EXISTS
FOR (o:Oferta) REQUIRE o.id IS UNIQUE;

CREATE CONSTRAINT curso_id IF NOT EXISTS
FOR (c:Curso) REQUIRE c.id IS UNIQUE;

// ===========================
// 2) Nodos: Empresas
// ===========================

MERGE (tech:Empresa {id:"emp-tech"}) 
SET tech.nombre="Tech Solutions", tech.industria="Software";

MERGE (data:Empresa {id:"emp-data"}) 
SET data.nombre="Data Corp", data.industria="Consultoría";

MERGE (innova:Empresa {id:"emp-innova"}) 
SET innova.nombre="Innovatech", innova.industria="Tecnología";

// ===========================
// 3) Nodos: Ofertas 
// ===========================

MERGE (ofBackend:Oferta {id:"of-backend"}) 
SET ofBackend.puesto="Desarrollador Backend", 
    ofBackend.ubicacion="Remoto", 
    ofBackend.modalidad="remoto",
    ofBackend.estado="abierta",
    ofBackend.requisitos=["Node.js", "Express", "MongoDB", "APIs REST"];

MERGE (ofAnalista:Oferta {id:"of-analista-datos"}) 
SET ofAnalista.puesto="Analista de Datos", 
    ofAnalista.ubicacion="CABA", 
    ofAnalista.modalidad="presencial",
    ofAnalista.estado="abierta",
    ofAnalista.requisitos=["SQL", "Power BI", "Python", "Estadística"];

MERGE (ofIA:Oferta {id:"of-especialista-ia"}) 
SET ofIA.puesto="Especialista en IA", 
    ofIA.ubicacion="CABA", 
    ofIA.modalidad="híbrido",
    ofIA.estado="abierta",
    ofIA.requisitos=["Machine Learning", "Python", "TensorFlow", "Análisis de datos"];


// ===========================
// 4) Nodos: Candidatos 
// ===========================

MERGE (rosario:Candidato {id:"cand-rosario"})
SET rosario.nombre="Rosario Martinez",
    rosario.estado="activo",
    rosario.residencia="CABA",
    rosario.habilidades=["SQL", "Power BI", "Excel", "Python"];

MERGE (marcos:Candidato {id:"cand-marcos"})
SET marcos.nombre="Marcos Pereyra",
    marcos.estado="activo",
    marcos.residencia="CABA",
    marcos.habilidades=["Node.js", "JavaScript", "MongoDB", "APIs REST"];

MERGE (camila:Candidato {id:"cand-camila"})
SET camila.nombre="Camila Gebara",
    camila.estado="activo",
    camila.residencia="Santa Fe",
    camila.habilidades=["Machine Learning", "Python", "TensorFlow", "Data Analysis"];

MERGE (lucia:Candidato {id:"cand-lucia"})
SET lucia.nombre="Lucía Fernández",
    lucia.estado="activo",
    lucia.residencia="CABA",
    lucia.habilidades=["Node.js", "Express", "MongoDB", "APIs REST"];

MERGE (julian:Candidato {id:"cand-julian"})
SET julian.nombre="Julián Torres",
    julian.estado="activo",
    julian.residencia="CABA",
    julian.habilidades=["SQL", "Power BI", "Python", "Estadística"];

MERGE (tomas:Candidato {id:"cand-tomas"})
SET tomas.nombre="Tomás Herrera",
    tomas.estado="activo",
    tomas.residencia="Santa Fe",
    tomas.habilidades=["Machine Learning", "Python", "TensorFlow", "Data Analysis"];

MERGE (valentina:Candidato {id:"cand-valentina"})
SET valentina.nombre="Valentina Ruiz",
    valentina.estado="activo",
    valentina.residencia="CABA",
    valentina.habilidades=["Node.js", "Express", "MongoDB", "APIs REST"];

MERGE (santiago:Candidato {id:"cand-santiago"})
SET santiago.nombre="Santiago López",
    santiago.estado="activo",
    santiago.residencia="CABA",
    santiago.habilidades=["SQL", "Power BI", "Python", "Estadística"];

// ===========================
// 5) Nodos: Cursos
// ===========================

MERGE (cursoNode:Curso {id:"curso-node"})
SET cursoNode.titulo="Node.js Avanzado", cursoNode.formato="video", cursoNode.duracion_h=15;

MERGE (cursoPowerBI:Curso {id:"curso-powerbi"})
SET cursoPowerBI.titulo="Power BI Avanzado", cursoPowerBI.formato="video", cursoPowerBI.duracion_h=10;

MERGE (cursoML:Curso {id:"curso-ml"})
SET cursoML.titulo="Machine Learning con Python", cursoML.formato="pdf", cursoML.duracion_h=20;

MERGE (cursoSQL:Curso {id:"curso-sql"})
SET cursoSQL.titulo="SQL Intermedio", cursoSQL.formato="live", cursoSQL.duracion_h=12;

MERGE (cursoComunicacion:Curso {id:"curso-comunicacion"})
SET cursoComunicacion.titulo="Comunicación Efectiva", cursoComunicacion.formato="video", cursoComunicacion.duracion_h=5;

// ============================================
// 1) Relaciones Candidato → Oferta (POSTULO_A)
// ============================================
MATCH (rosario:Candidato {id:"cand-rosario"}), (ofBackend:Oferta {id:"of-backend"})
MERGE (rosario)-[:POSTULO_A {estado:"aplicado", fecha:"2025-10-16"}]->(ofBackend);

MATCH (marcos:Candidato {id:"cand-marcos"}), (ofAnalista:Oferta {id:"of-analista-datos"})
MERGE (marcos)-[:POSTULO_A {estado:"en_proceso", fecha:"2025-10-15"}]->(ofAnalista);

MATCH (camila:Candidato {id:"cand-camila"}), (ofIA:Oferta {id:"of-especialista-ia"})
MERGE (camila)-[:POSTULO_A {estado:"rechazado", fecha:"2025-10-14"}]->(ofIA);

MATCH (lucia:Candidato {id:"cand-lucia"}), (ofBackend:Oferta {id:"of-backend"})
MERGE (lucia)-[:POSTULO_A {estado:"en_proceso", fecha:"2025-10-20"}]->(ofBackend);

MATCH (julian:Candidato {id:"cand-julian"}), (ofAnalista:Oferta {id:"of-analista-datos"})
MERGE (julian)-[:POSTULO_A {estado:"aplicado", fecha:"2025-10-18"}]->(ofAnalista);

MATCH (tomas:Candidato {id:"cand-tomas"}), (ofIA:Oferta {id:"of-especialista-ia"})
MERGE (tomas)-[:POSTULO_A {estado:"aplicado", fecha:"2025-10-19"}]->(ofIA);

MATCH (valentina:Candidato {id:"cand-valentina"}), (ofBackend:Oferta {id:"of-backend"})
MERGE (valentina)-[:POSTULO_A {estado:"aplicado", fecha:"2025-10-21"}]->(ofBackend);

MATCH (santiago:Candidato {id:"cand-santiago"}), (ofAnalista:Oferta {id:"of-analista-datos"})
MERGE (santiago)-[:POSTULO_A {estado:"en_proceso", fecha:"2025-10-22"}]->(ofAnalista);

// ========================================
// 2) Relaciones Empresa → Oferta (PUBLICO)
// ========================================
MATCH (tech:Empresa {id:"emp-tech"}), (ofBackend:Oferta {id:"of-backend"})
MERGE (tech)-[:PUBLICO {fecha_publicacion:"2025-10-01", requisitos:["JavaScript","Node.js"]}]->(ofBackend);

MATCH (data:Empresa {id:"emp-data"}), (ofAnalista:Oferta {id:"of-analista-datos"})
MERGE (data)-[:PUBLICO {fecha_publicacion:"2025-10-02", requisitos:["SQL","Excel"]}]->(ofAnalista);

MATCH (innova:Empresa {id:"emp-innova"}), (ofIA:Oferta {id:"of-especialista-ia"})
MERGE (innova)-[:PUBLICO {fecha_publicacion:"2025-10-03", requisitos:["Python","Machine Learning"]}]->(ofIA);

// =========================================================
// 3) Relaciones Candidato → Curso (COMPLETO / INSCRIPTO_EN)
// =========================================================
MATCH (rosario:Candidato {id:"cand-rosario"}), (cursoNode:Curso {id:"curso-node"})
MERGE (rosario)-[:COMPLETO {nota:9, fecha_inicio:"2025-08-01", fecha_fin:"2025-08-16"}]->(cursoNode);

MATCH (marcos:Candidato {id:"cand-marcos"}), (cursoPowerBI:Curso {id:"curso-powerbi"})
MERGE (marcos)-[:INSCRIPTO_EN {progreso:50, fecha_inicio:"2025-09-01"}]->(cursoPowerBI);

MATCH (camila:Candidato {id:"cand-camila"}), (cursoML:Curso {id:"curso-ml"})
MERGE (camila)-[:INSCRIPTO_EN {progreso:30, fecha_inicio:"2025-09-05"}]->(cursoML);

// ==============================================
// 4) Relaciones Candidato → Empresa (TRABAJO_EN)
// ==============================================
MATCH (rosario:Candidato {id:"cand-rosario"}), (tech:Empresa {id:"emp-tech"})
MERGE (rosario)-[:TRABAJO_EN {puesto:"Junior Developer", fecha_desde:"2023-01-01", fecha_hasta:"2024-12-31"}]->(tech);

MATCH (marcos:Candidato {id:"cand-marcos"}), (data:Empresa {id:"emp-data"})
MERGE (marcos)-[:TRABAJO_EN {puesto:"Analista de Datos", fecha_desde:"2022-06-01", fecha_hasta:"2024-06-30"}]->(data);

// ====================================================================
// 5) Relaciones Candidato → Candidato (CONTACTO_CON / RECOMENDADO_POR)
// ====================================================================
MATCH (rosario:Candidato {id:"cand-rosario"}), (marcos:Candidato {id:"cand-marcos"})
MERGE (rosario)-[:CONTACTO_CON {tipo_contacto:"compañero", fecha_desde:"2023-02-01"}]->(marcos);

MATCH (camila:Candidato {id:"cand-camila"}), (rosario:Candidato {id:"cand-rosario"})
MERGE (camila)-[:RECOMENDADO_POR {motivo:"proyecto compartido"}]->(rosario);

// ===============================================
// 6) Relaciones Oferta → Curso (REQUERIMIENTO_DE)
// ===============================================
MATCH (ofBackend:Oferta {id:"of-backend"}), (cursoNode:Curso {id:"curso-node"})
MERGE (ofBackend)-[:REQUERIMIENTO_DE {nivel_recomendado:"intermedio"}]->(cursoNode);

MATCH (ofAnalista:Oferta {id:"of-analista-datos"}), (cursoPowerBI:Curso {id:"curso-powerbi"})
MERGE (ofAnalista)-[:REQUERIMIENTO_DE {nivel_recomendado:"avanzado"}]->(cursoPowerBI);

// ============================================
// 7) Relaciones Empresa → Candidato (CONTRATA)
// ============================================
MATCH (tech:Empresa {id:"emp-tech"}), (rosario:Candidato {id:"cand-rosario"})
MERGE (tech)-[:CONTRATA {puesto:"Junior Developer", fecha_desde:"2023-01-01"}]->(rosario);