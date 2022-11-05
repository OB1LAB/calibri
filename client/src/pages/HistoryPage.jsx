import React, { useState, useEffect, useContext } from "react";
import HistoryBuyTable from "../components/tables/HistoryBuy";
import HistoryVacationTable from "../components/tables/HistoryVacation";
import HistoryViolationsTable from "../components/tables/HistoryViolations";
import SelectServer from "../components/Selectors/SelectServer";
import HistoryService from "../services/HistoryService";
import Loader from "../components/Loader/Loader";
import { Context } from "..";
import "../styles/History.css";

export default function HistoryPage() {
  let server = "";
  const { store } = useContext(Context);
  const [data, setData] = useState({});

  if (store.user["dt"]["lvl"] > 1 && store.user["tmrpg"]["lvl"] > 1) {
    server = "dt";
  } else {
    if (store.user["dt"]["lvl"] > 1) {
      server = "dt";
    } else if (store.user["tmrpg"]["lvl"] > 1) {
      server = "tmrpg";
    }
  }
  const [selectedServer, setselectedServer] = useState(server);

  useEffect(() => {
    const tables = document.querySelectorAll("[id=history]");
    tables.forEach((table) => {
      const scrollHeight = table.scrollHeight;
      const height = table.clientHeight;
      const maxScrollTop = scrollHeight - height;
      table.scrollTop = maxScrollTop > 0 ? maxScrollTop : 0;
    });
  }, [selectedServer]);

  useEffect(() => {
    const setHistory = async () => {
      const response = await HistoryService.fetchHistory();
      response && setData(response.data);
      const tables = document.querySelectorAll("[id=history]");
      tables.forEach((table) => {
        const scrollHeight = table.scrollHeight;
        const height = table.clientHeight;
        const maxScrollTop = scrollHeight - height;
        table.scrollTop = maxScrollTop > 0 ? maxScrollTop : 0;
      });
    };
    setHistory();
    document.title = "История & Выдача";
  }, []);

  if (Object.keys(data).length === 0) {
    return <Loader />;
  }

  return (
    <div className="tables">
      <div className="selectServer">
        {store.user["dt"]["lvl"] > 1 && store.user["tmrpg"]["lvl"] > 1 && (
          <SelectServer
            onChange={({ value }) => {
              setselectedServer(value);
            }}
          />
        )}
      </div>
      <div className="up">
        <HistoryVacationTable
          user={store.user}
          data={data[selectedServer]["vacation"]}
          selectedServer={selectedServer}
          setData={setData}
        />
        <HistoryViolationsTable
          data={data[selectedServer]["violation"]}
          user={store.user}
          selectedServer={selectedServer}
          setData={setData}
        />
      </div>
      <div className="down">
        <HistoryBuyTable
          setData={setData}
          data={data[selectedServer]["buy"]}
          user={store.user}
        />
      </div>
    </div>
  );
}
