import { useState, useEffect } from "react";
import Loader from "../Loader/Loader";
import LogsService from "../../services/LogsService";
import classes from "./Admin.module.css";

export default function Logs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const getLogs = async () => {
      const response = await LogsService.fetchLogs();
      response && setLogs(response.data);
    };
    getLogs();
  }, []);

  if (logs.length === 0) {
    return <Loader />;
  }

  return (
    <div className={classes.logs}>
      <div className={classes.logsContent}>
        {logs.map((log, index) => {
          return <div key={index}>{log}</div>;
        })}
      </div>
    </div>
  );
}
