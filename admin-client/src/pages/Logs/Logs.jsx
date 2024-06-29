import React, { useState, useEffect } from "react";
import { getToken } from "../../utils/jwtToken";
import "./index.css";

function Logs() {
  const [file, setFile] = useState("");

  useEffect(() => {
    getLogs();
  }, []);

  const getLogs = () => {
    getToken().then((token) => {
      const headers = { Authorization: `Bearer ${token}` };
      fetch("http://kematin.space:9999/admin/logs", { headers: headers })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.text();
        })
        .then((data) => {
          setFile(data);
        })
        .catch((error) => {
          console.error("Error fetching logs:", error);
        });
    });
  };

  return (
    <div id="logs">
      <h1>Логи</h1>
      <textarea className="logs" defaultValue={file}></textarea>
    </div>
  );
}

export default Logs;
