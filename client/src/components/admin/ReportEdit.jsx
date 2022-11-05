import React, { useState, useContext } from "react";
import ReportService from "../../services/ReportService";
import Selector from "../Selectors/Selector";
import SelectServer from "../Selectors/SelectServer";
import Modal from "../modal/Modal";
import { Context } from "../..";
import classes from "./Admin.module.css";

const actions = [
  { value: "Monday", label: "Понедельник", number: 0 },
  { value: "Tuesday", label: "Вторник", number: 1 },
  { value: "Wednesday", label: "Среда", number: 2 },
  { value: "Thursday", label: "Четверг", number: 3 },
  { value: "Friday", label: "Пятница", number: 4 },
  { value: "Saturday", label: "Суббота", number: 5 },
  { value: "Sunday", label: "Воскресенье", number: 6 },
];

export default function ReportEdit() {
  let server = "";
  const { store } = useContext(Context);
  const [modal, setModal] = useState(false);
  const [days, setDays] = useState([0, 1, 2, 3, 4, 5, 6]);

  if (store.user["dt"]["lvl"] > 4 && store.user["tmrpg"]["lvl"] > 4) {
    server = "dt";
  } else {
    if (store.user["dt"]["lvl"] > 4) {
      server = "dt";
    } else if (store.user["tmrpg"]["lvl"] > 4) {
      server = "tmrpg";
    }
  }
  const [selectedServer, setSelectedServer] = useState(server);

  const editReport = async () => {
    let reportDays = days;
    reportDays.length === 0 && (reportDays = [0, 1, 2, 3, 4, 5, 6]);
    await ReportService.editReport(selectedServer, reportDays);
    setModal(true);
  };
  return (
    <div style={{ width: "100%" }}>
      {store.user["dt"]["lvl"] > 4 && store.user["tmrpg"]["lvl"] > 4 && (
        <SelectServer onChange={(value) => setSelectedServer(value.value)} />
      )}
      <div className={classes.report}>
        <div className={classes.selector}>
          <Selector
            options={actions}
            isMulti={true}
            closeMenuOnSelect={false}
            placeholder="Выбрать дни"
            onChange={(value) =>
              setDays(
                value.map((day) => {
                  return day.number;
                })
              )
            }
          />
        </div>
        <button onClick={() => editReport()}>Изменить</button>
      </div>
      <Modal visible={modal} setVisible={setModal}>
        <div className={classes.reportModal}>
          <span>Отчёт успешно изменён</span>
        </div>
      </Modal>
    </div>
  );
}
