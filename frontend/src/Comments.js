import { useEffect, useState } from "react";
import axios from "axios";

function Comments({ photoId, token }) {

  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");

  // cargar comentarios
  useEffect(() => {

    axios.get(
      `http://127.0.0.1:8000/api/interactions/comments/${photoId}/`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    .then(res => setComments(res.data));

  }, [photoId, token]);

  // enviar comentario
  const handleComment = () => {

    if (!text.trim()) return; // evitar comentarios vacíos

    axios.post(
      `http://127.0.0.1:8000/api/interactions/comments/${photoId}/`,
      { text },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    .then(res => {
      setComments(prev => [res.data, ...prev]);
      setText("");
    });

  };

  return (
    <div>

      <h4>Comentarios</h4>

      {comments.map(c => (
        <p key={c.id}>
          <b>{c.user}</b>: {c.text}
        </p>
      ))}

      <input
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Escribe un comentario..."
      />

      <button onClick={handleComment}>
        Enviar
      </button>

    </div>
  );
}

export default Comments;
