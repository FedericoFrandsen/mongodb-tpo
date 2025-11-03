import { useState } from "react";
import UserSearch from "../components/UserSearch";
import UpdateUser from "../components/UpdateUser";
import DeleteUser from "../components/DeleteUser";
import AddCapacitacion from "../components/AddCapacitacion";
import GetVersion from "../components/GetVersion";

export default function UserManagementPage() {
  const [usuario, setUsuario] = useState(null);

  const handleSelect = (user) => setUsuario(user);
  const handleDeleted = () => setUsuario(null);

  return (
    <div>
      <UserSearch onSelect={handleSelect} />
      {usuario && (
        <>
          <UpdateUser nombre={usuario.informacion_personal.nombre_apellido} />
          <DeleteUser nombre={usuario.informacion_personal.nombre_apellido} onDeleted={handleDeleted} />
          <AddCapacitacion nombre={usuario.informacion_personal.nombre_apellido} />
          <GetVersion nombre={usuario.informacion_personal.nombre_apellido} />
        </>
      )}
    </div>
  );
}