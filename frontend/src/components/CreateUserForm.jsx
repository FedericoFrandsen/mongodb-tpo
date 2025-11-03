// Este componente sirve para crear un nuevo usuario, enviando los datos al backend FastAPI (endpoint /users)

import { useState } from "react";
import api from "../api";

export default function CreateUserForm() {
  const [form, setForm] = useState({
    nombre: "",
    email: "",
    skills: "",
  });

  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    setError("");

    try {
      // Convertir skills (string separadas por coma) → array
      const skillsArray = form.skills
        .split(",")
        .map((s) => s.trim().toLowerCase())
        .filter((s) => s);

      const nuevoUsuario = {
        nombre: form.nombre.trim().toLowerCase(),
        email: form.email.trim(),
        skills: skillsArray,
      };

      const res = await api.post("/users", nuevoUsuario);

      if (res.data.ok) {
        setMensaje(`✅ Usuario "${res.data.user}" creado con éxito`);
        setForm({ nombre: "", email: "", skills: "" });
      } else {
        setError("❌ No se pudo crear el usuario");
      }
    } catch (err) {
      console.error(err);
      if (err.response?.status === 409) {
        setError("⚠️ El usuario ya existe");
      } else {
        setError("❌ Error al crear usuario");
      }
    }
  };

  return (
    <div className="card">
      <h3>Registrar nuevo usuario</h3>
      <form onSubmit={handleSubmit}>
        <input
          name="nombre"
          placeholder="Nombre y apellido"
          value={form.nombre}
          onChange={handleChange}
          required
        />
        <input
          name="email"
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <input
          name="skills"
          placeholder="Habilidades (separadas por coma)"
          value={form.skills}
          onChange={handleChange}
        />
        <button type="submit">Crear usuario</button>
      </form>

      {mensaje && <p style={{ color: "green" }}>{mensaje}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
