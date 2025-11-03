import { useState } from "react";
import api from "../api";

export default function GetVersion({ nombre }) {
  const [versiones, setVersiones] = useState([]);

  const handleClick = async () => {
    if (!nombre) return;
    try {
      const res = await api.get(`/users/${nombre}/versiones`);
      setVersiones(res.data.versiones || []);
    } catch (err) {
      console.error(err);
      alert("❌ Error al obtener versiones");
    }
  };

  if (!nombre) return null;

  return (
    <div className="card">
      <h3>Historial de versiones</h3>
      <button className="small-btn" onClick={handleClick}>Ver versiones</button>

      {versiones.length > 0 && (
        <div className="versiones-container">
          {versiones.map((v, i) => (
            <div key={i} className="version-item">
              <div className="version-header">
                <strong>Versión {v.version}</strong> — {v.cambio}
              </div>
              {v.diff && Object.keys(v.diff).length > 0 && (
                <table className="diff-table">
                  <thead>
                    <tr>
                      <th>Campo</th>
                      <th>Valor</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(v.diff).map(([campo, valor]) => (
                      <tr key={campo}>
                        <td>{campo}</td>
                        <td>
                          {typeof valor === "object" ? JSON.stringify(valor) : valor}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}