import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from "react";
import axios from "axios";

function App() {

  const [photos, setPhotos] = useState([]);

  useEffect(() => {

    const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzczODI4MTAwLCJpYXQiOjE3NzM4MjYzMDEsImp0aSI6IjVlMTY0NmU4Y2IzMjQyNDZiZWRlM2RjMGE4N2Y0MzEyIiwidXNlcl9pZCI6IjIiLCJ1c2VybmFtZSI6InVzdWFyaW8xIn0.FV7PfFYfJk4dVHpy7UCm6RThLMGFZwdhA6tqHrE494g";

    axios({
      method: "GET",
      url: "http://127.0.0.1:8000/api/photos/feed/",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/json",
        "Content-Type": "application/json"
      }
    })
    .then(res => {
      console.log("DATA RECIBIDA:", res.data);
      setPhotos(res.data);
    })
    .catch(err => {
      console.error("ERROR AXIOS:", err);
    });

  }, []);

  return (
    <div>
      <h1>Feed</h1>

      {photos.map(photo => (
        <div key={photo.id}>
          <p>{photo.caption}</p>
          <p>❤️ {photo.likes_count}</p>
          <p>💬 {photo.comments_count}</p>
          <hr />
        </div>
      ))}

    </div>
  );
}

export default App;
