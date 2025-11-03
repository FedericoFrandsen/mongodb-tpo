// Este componente actualiza un usuario (email, celular, residencia)

import { useState } from "react";
import api from "../api";

export default function UpdateUser({ nombre }) {
  const [form, setForm] = useState({ email: "", celular: "", residencia: "" });
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    setError("");

    try {
      const res = await api.put(`/users/${nombre}`, form);
      if (res.data.ok) {
        setMensaje("✅ Usuario actualizado");
      } else {
        setError("❌ No se pudo actualizar usuario");
      }
    } catch (err) {
      console.error(err);
      setError("❌ Error al actualizar usuario");
    }
  };

  if (!nombre) return null; // no renderizar si no hay usuario seleccionado

  return (
    <div className="card">
      <h3>Actualizar usuario</h3>
      <form onSubmit={handleSubmit}>
        <input name="email" placeholder="Nuevo email" value={form.email} onChange={handleChange} />
        <input name="celular" placeholder="Nuevo celular" value={form.celular} onChange={handleChange} />
        <input name="residencia" placeholder="Nueva residencia" value={form.residencia} onChange={handleChange} />
        <button type="submit">Actualizar</button>
      </form>
      {mensaje && <p style={{ color: "green" }}>{mensaje}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}