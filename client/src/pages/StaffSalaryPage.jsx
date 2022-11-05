import React, { useEffect, useState, useContext } from "react";
import SelectServer from "../components/Selectors/SelectServer";
import StaffSalary from "../components/tables/StaffSalary";
import CriteriaSalary from "../components/criterias/CriteriaSalary";
import CriteriaViolations from "../components/criterias/CriteriaViolations";
import Loader from "../components/Loader/Loader";
import "../styles/StaffSalary.css";
import { Context } from "..";
import SalaryService from "../services/SalaryService";

export default function StaffSalaryPage() {
  let server = "";
  const { store } = useContext(Context);
  const [staffData, setStaffData] = useState({});

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
    const setData = async () => {
      const response = await SalaryService.fetchSalary();
      response && setStaffData(response.data);
    };
    setData();
    document.title = "Зп состава";
  }, []);

  if (Object.keys(staffData).length === 0) {
    return <Loader />;
  }

  return (
    <div>
      {store.user["dt"]["lvl"] > 1 && store.user["tmrpg"]["lvl"] > 1 && (
        <SelectServer
          onChange={({ value }) => {
            setselectedServer(value);
          }}
        />
      )}
      <StaffSalary
        user={store.user}
        selectedServer={selectedServer}
        staffData={staffData[selectedServer]}
        setData={setStaffData}
      />
      <div className="criteries">
        <CriteriaSalary />
        <CriteriaViolations />
      </div>
    </div>
  );
}
