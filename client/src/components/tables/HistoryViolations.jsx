import { useState } from "react";
import classes from "./History.module.css";
import Modal from "../modal/Modal";
import ViolationService from "../../services/ViolationService";

export default function HistoryViolationsTable({
  data,
  user,
  selectedServer,
  setData,
}) {
  const [name, setName] = useState("None");
  const [deleteId, setDeleteId] = useState(0);
  const [modal, setModal] = useState(false);

  const deleteViolation = async () => {
    const response = await ViolationService.deleteViolation(
      deleteId,
      selectedServer
    );
    response && setData(response.data);
  };

  return (
    <div className={classes.access}>
      <h2>История нарушений</h2>
      <p>История нарушений не очищается</p>
      <table
        className={`${classes.generalTable} ${classes.historyViolations}`}
        id="history"
      >
        <thead>
          <tr>
            <td>Никнейм модератора</td>
            <td>Дата получения</td>
            <td>Вид/Причина</td>
          </tr>
        </thead>
        <tbody>
          {data.map((value) => {
            return (
              <tr key={value.id}>
                {user["max_role"]["lvl"] > 4 ? (
                  <td>
                    <button
                      onClick={() => {
                        setDeleteId(value.id);
                        setName(value.user);
                        setModal(true);
                      }}
                    >
                      {value.user}
                    </button>
                  </td>
                ) : (
                  <td>{value.user}</td>
                )}
                <td>{value.date}</td>
                <td>{value.cause}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <Modal visible={modal} setVisible={setModal}>
        <h1>Вы точно хотите удалить отпуск у {name}?</h1>
        <div className={classes.group}>
          <button
            onClick={() => {
              deleteViolation();
              setModal(false);
            }}
            className={classes.buttonGreen}
          >
            Да
          </button>
          <button
            onClick={() => {
              setModal(false);
            }}
            className={classes.buttonRed}
          >
            Нет
          </button>
        </div>
      </Modal>
    </div>
  );
}
