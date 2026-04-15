import { useState } from "react";
import axios from "axios";

function Login({ setToken }) {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {

    axios.post("http://127.0.0.1:8000/api/token/", {
      username,
      password
    })
    .then(res => {
      console.log(res.data);

      localStorage.setItem("token", res.data.access);
      setToken(res.data.access);
    })
    .catch(err => console.log(err));

  };

  return (
    <div>
      <h2>Login</h2>

      <input
        placeholder="username"
        onChange={e => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="password"
        onChange={e => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>
        Login
      </button>
    </div>
  );
}

export default Login;
