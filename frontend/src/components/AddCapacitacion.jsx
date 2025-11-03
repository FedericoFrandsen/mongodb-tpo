// Este componente agrega una capacitación 

import { useState } from "react";
import api from "../api";

export default function AddCapacitacion({ nombre }) {
  const [capacitacion, setCapacitacion] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!nombre || !capacitacion) return;

    try {
      const res = await api.post("/users/capacitacion", { nombre, capacitacion });
      alert(res.data.message);
      setCapacitacion("");
    } catch (err) {
      console.error(err);
      alert("❌ Error al agregar capacitación");
    }
  };

  if (!nombre) return null;
  return (
    <div className="card">
      <h3>Agregar capacitación</h3>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Nombre de la capacitación"
          value={capacitacion}
          onChange={(e) => setCapacitacion(e.target.value)}
        />
        <button type="submit">Agregar</button>
      </form>
    </div>
  );
}