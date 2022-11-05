import React, { useEffect, useState, useContext } from "react";
import SelectServer from "../components/Selectors/SelectServer";
import StaffList from "../components/admin/StaffList";
import SelectAction from "../components/Selectors/SelectAction";
import UserService from "../services/UserService";
import { Context } from "..";
import Logs from "../components/admin/Logs";
import ReportEdit from "../components/admin/ReportEdit";
import "../styles/Admin.css";

export default function AdminPage() {
  let server = "";
  const { store } = useContext(Context);
  const [staff, setStaff] = useState([]);
  const [action, setAction] = useState("appointment");

  if (store.user["dt"]["lvl"] > 4 && store.user["tmrpg"]["lvl"] > 4) {
    server = {
      value: "dt",
      label: "DraconicTech",
    };
  } else {
    if (store.user["dt"]["lvl"] > 4) {
      server = {
        value: "dt",
        label: "DraconicTech",
      };
    } else if (store.user["tmrpg"]["lvl"] > 4) {
      server = {
        value: "tmrpg",
        label: "TechnoMagicRPG",
      };
    }
  }
  const [selectedServer, setselectedServer] = useState(server);

  useEffect(() => {
    document.title = "Админ панель";
    const getUsers = async () => {
      const response = await UserService.fetchUsers();
      response && setStaff(response.data);
    };
    getUsers();
  }, []);

  return (
    <div className="adminPage">
      <div className="selectAction">
        <SelectAction onChange={setAction} />
      </div>
      {(action === "appointment" && (
        <div style={{ width: "1400px" }}>
          {store.user["dt"]["lvl"] > 4 && store.user["tmrpg"]["lvl"] > 4 && (
            <SelectServer
              value={selectedServer}
              onChange={(value) => {
                setselectedServer(value);
              }}
            />
          )}
          <StaffList
            staffData={staff}
            user={store.user}
            selectedServer={selectedServer.value}
            setStaff={setStaff}
          />
        </div>
      )) ||
        (action === "logs" && <Logs />) ||
        (action === "reportEdit" && <ReportEdit />)}
    </div>
  );
}
