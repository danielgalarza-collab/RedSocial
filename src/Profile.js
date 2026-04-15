import { useEffect, useState } from "react";
import axios from "axios";

function Profile({ userId, token, onMessage }) {

  const [profile, setProfile] = useState(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/api/interactions/users/${userId}/profile/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => setProfile(res.data));
  }, [userId, token]);

  if (!profile) return <p>Cargando...</p>;

  return (
    <div>
      <img 
        src={profile.avatar} 
        alt="avatar" 
        style={{ width: "100px", borderRadius: "50%" }}
      />

      <h2>{profile.username}</h2>
      <p>{profile.bio}</p>

      <button onClick={() => onMessage(userId)}>
        Enviar mensaje
      </button>

      <h3>Fotos</h3>
      {profile.photos.map(p => (
        <img 
          key={p.id}
          src={p.image}
          alt=""
          style={{ width: "150px", margin: "5px" }}
        />
      ))}
    </div>
  );
}

export default Profile;
