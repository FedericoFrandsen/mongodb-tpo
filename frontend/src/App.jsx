import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RegisterPage from "./pages/RegisterPage";
import UserManagementPage from "./pages/UserManagementPage";
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Contenedor de botones arriba */}
        <div className="header-buttons">
          <Link to="/">Registrar Usuario</Link>
          <Link to="/users">Gestionar Usuario</Link>
        </div>

        {/* Contenedor principal de contenido */}
        <div className="main-content">
          <Routes>
            <Route path="/" element={<RegisterPage />} />
            <Route path="/users" element={<UserManagementPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;