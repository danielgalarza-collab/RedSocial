import { useState, useEffect } from "react";
import api from "./api";

import Login from "./Login";
import Comments from "./Comments";
import Conversations from "./Conversations";
import Chat from "./Chat";
import Profile from "./Profile";

function App() {

  const [token, setToken] = useState(localStorage.getItem("token"));
  const [photos, setPhotos] = useState([]);

  // conversación seleccionada
  const [selectedConversation, setSelectedConversation] = useState(null);

  // LISTA GLOBAL DE CONVERSACIONES
  const [conversations, setConversations] = useState([]);

  //  CONTADOR DE NOTIFICACIONES
  const [notificationCount, setNotificationCount] = useState(0);

  //  Función para marcar notificaciones como leídas
  const markNotificationsAsRead = () => {
    api.post("interactions/notifications/read/")
      .then(() => {
        setNotificationCount(0); // vaciar contador
      });
  };

  //  Cargar notificaciones al inicio
  useEffect(() => {
    if (token) {
      api.get("interactions/notifications/")
        .then(res => {
          const unread = res.data.filter(n => !n.is_read).length;
          setNotificationCount(unread);
        });
    }
  }, [token]);

  // Cargar conversaciones al inicio
  useEffect(() => {
    if (token) {
      api.get("interactions/chat/conversations/")
        .then(res => setConversations(res.data));
    }
  }, [token]);

  // Función para crear o obtener una conversación
  const startConversation = (otherUserId) => {
    api.post("interactions/chat/start/", { user_id: otherUserId })
      .then(res => {
        const conversationId = res.data.conversation_id;

        // Seleccionar conversación
        setSelectedConversation(conversationId);

        // Opcional: moverla al tope si ya existe
        setConversations(prev => {
          const exists = prev.find(c => c.id === conversationId);
          if (exists) return prev;
          return prev; // ya se actualizará sola cuando llegue el primer mensaje
        });
      });
  };

  // cargar feed
  useEffect(() => {
    if (token) {
      api.get("photos/feed/")
        .then(res => setPhotos(res.data));
    }
  }, [token]);

  // dar like
  const handleLike = (photoId) => {
    api.post(`interactions/like/${photoId}/`)
      .then(res => {
        setPhotos(prev =>
          prev.map(p =>
            p.id === photoId
              ? {
                  ...p,
                  likes_count: res.data.liked
                    ? p.likes_count + 1
                    : p.likes_count - 1,
                  is_liked: res.data.liked
                }
              : p
          )
        );
      });
  };

  // si no hay token → login
  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <div>
      <h1>Feed</h1>

      {/*  ICONO DE NOTIFICACIONES (clicable) */}
      <div
        onClick={markNotificationsAsRead}
        style={{
          position: "relative",
          display: "inline-block",
          marginBottom: "20px",
          cursor: "pointer"
        }}
      >
        <span style={{ fontSize: "24px" }}>🔔</span>

        {notificationCount > 0 && (
          <span
            style={{
              position: "absolute",
              top: "-5px",
              right: "-10px",
              background: "red",
              color: "white",
              borderRadius: "50%",
              padding: "2px 6px",
              fontSize: "12px"
            }}
          >
            {notificationCount}
          </span>
        )}
      </div>

      {photos.map(photo => (
        <div key={photo.id} style={{ marginBottom: "20px" }}>

          <p>{photo.caption}</p>

          <img 
            src={photo.image} 
            alt="foto" 
            style={{ width: "300px", borderRadius: "10px" }}
          />

          <p>
            ❤️ {photo.likes_count}

            <button 
              onClick={() => handleLike(photo.id)} 
              style={{ marginLeft: "10px" }}
            >
              {photo.is_liked ? "💖 Unlike" : "🤍 Like"}
            </button>
          </p>

          <Comments photoId={photo.id} token={token} />

          <hr />
        </div>
      ))}

      {/* Perfil de prueba */}
      <Profile 
        userId={1} 
        token={token} 
        onMessage={startConversation}
      />

      {/* Sección de mensajes */}
      <h1>Mensajes</h1>

      <Conversations 
        token={token}
        conversations={conversations}
        onSelect={setSelectedConversation}
      />

      {selectedConversation && (
        <Chat 
          conversationId={selectedConversation}
          token={token}
          conversations={conversations}
          setConversations={setConversations}
        />
      )}

    </div>
  );
}

export default App;
