// Este componente sirve para buscar un usuario

import { useState } from "react";
import api from "../api";

export default function UserSearch({ onSelect }) {
  const [nombre, setNombre] = useState("");
  const [usuario, setUsuario] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setUsuario(null);
    setError("");

    try {
      const res = await api.get(`/users/${nombre.trim().toLowerCase()}`);
      if (res.data.error) {
        setError("❌ Usuario no encontrado");
      } else {
        setUsuario(res.data);
        if (onSelect) onSelect(res.data); // pasa usuario seleccionado al padre
      }
    } catch (err) {
      console.error(err);
      setError("❌ Error al buscar usuario");
    }
  };

  return (
    <div className="card">
      <h3>Buscar usuario por nombre</h3>
      <form onSubmit={handleSubmit}>
        <input
          name="nombre"
          placeholder="Nombre y apellido"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
        />
        <button type="submit">Buscar</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {usuario && (
        <div className="user-details">
            <p><strong>Nombre:</strong> {usuario.informacion_personal.nombre_apellido}</p>
            <p><strong>Email:</strong> {usuario.informacion_personal.email}</p>
            <p><strong>Celular:</strong> {usuario.informacion_personal.celular}</p>
            <p><strong>Residencia:</strong> {usuario.informacion_personal.residencia}</p>
            <p><strong>Skills:</strong> {usuario.skills?.join(", ")}</p>
            <p><strong>Capacitaciones:</strong> {usuario.capacitaciones?.join(", ")}</p>
        </div>
        )}
    </div>
  );
}