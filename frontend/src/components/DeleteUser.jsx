// Este componente elimina un usuario

import api from "../api";

export default function DeleteUser({ nombre, onDeleted }) {
  const handleDelete = async () => {
    if (!window.confirm(`¿Eliminar usuario ${nombre}?`)) return;

    try {
      const res = await api.delete(`/users/${nombre}`);
      if (res.data.deleted > 0) {
        alert("✅ Usuario eliminado");
        if (onDeleted) onDeleted();
      } else {
        alert("❌ No se pudo eliminar usuario");
      }
    } catch (err) {
      console.error(err);
      alert("❌ Error al eliminar usuario");
    }
  };

  return (
    <button type="button" onClick={handleDelete}>
      Eliminar Usuario
    </button>
  );
}