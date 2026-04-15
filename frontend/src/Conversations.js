function Conversations({ conversations, onSelect, setConversations }) {

  const openConversation = (id) => {
    // Seleccionar conversación
    onSelect(id);

    // Marcar como leído
    setConversations(prev =>
      prev.map(conv =>
        conv.id === id
          ? { ...conv, unread_count: 0 }
          : conv
      )
    );

    // Reordenar por último mensaje
    setConversations(prev =>
      [...prev].sort((a, b) =>
        new Date(b.last_message?.created_at) - new Date(a.last_message?.created_at)
      )
    );
  };

  return (
    <div className="conversations-list">
      {conversations.map(conv => (
        <div
          key={conv.id}
          className="conversation-item"
          onClick={() => openConversation(conv.id)}
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            padding: "10px",
            borderBottom: "1px solid #ddd",
            cursor: "pointer"
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
	// punto online ofline
            <span
              style={{
                color: conv.other_user?.is_online ? "limegreen" : "gray",
                fontSize: "14px",
                marginRight: "6px"
              }}
            >
              ●
            </span>

            <div>
              <strong>{conv.name}</strong>
              <p style={{ margin: 0, color: "#666" }}>
                {conv.last_message?.text || "Sin mensajes aún"}
              </p>
            </div>
          </div>
	// numero de mensajes no leidos 
          {conv.unread_count > 0 && (
            <span
              style={{
                background: "#007bff",
                color: "white",
                padding: "4px 8px",
                borderRadius: "12px",
                fontSize: "12px",
                minWidth: "20px",
                textAlign: "center"
              }}
            >
              {conv.unread_count}
            </span>
          )}
        </div>
      ))}
    </div>
  );
}

export default Conversations;
