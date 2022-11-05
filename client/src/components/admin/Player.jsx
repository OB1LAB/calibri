import Modal from "../modal/Modal";
import { useState } from "react";
import classes from "./Admin.module.css";
import PlayerEdit from "./PlayerEdit";
import Vacation from "./Vacation";
import Violation from "./Violation";

export default function Player({ playerData, user, selectedServer, setStaff }) {
  const [responseModal, setResponseModal] = useState(false);
  const [responseData, setResponseData] = useState({
    color: "",
    content: "",
  });
  const [name, setName] = useState(playerData.name);
  const [discord, setDiscord] = useState(playerData.discord);
  const [role, setRole] = useState(playerData[selectedServer]["lvl"]);
  const [balance, setBalance] = useState(playerData.balance);
  const [birthday, setBirthday] = useState(playerData.birthday);
  const [editPlayer, setEditPlayer] = useState(false);
  const [vacation, setVacation] = useState(false);
  const [violation, setViolation] = useState(false);

  return (
    <div className={classes.player}>
      <img
        alt=""
        src={`https://skins.mcskill.net/?name=${playerData.name}&mode=1&fx=64&fy=128`}
      ></img>
      <div className={classes.information}>
        <p>Name: {playerData.name}</p>
        <p>DT: {playerData["dt"]["viewName"]}</p>
        <p>TMRPG: {playerData["tmrpg"]["viewName"]}</p>
        <p>Balance: {playerData.balance}</p>
        {user[selectedServer]["lvl"] > playerData[selectedServer]["lvl"] &&
          user[selectedServer]["lvl"] >= 5 && (
            <div className={classes.act}>
              <button
                onClick={() => {
                  setName(playerData.name);
                  setDiscord(playerData.discord);
                  setRole(playerData[selectedServer]["lvl"]);
                  setBalance(playerData.balance);
                  setBirthday(playerData.birthday);
                  setEditPlayer(true);
                }}
              >
                Редактировать
              </button>
              <button onClick={() => setVacation(true)}>Отпуск</button>
              <button onClick={() => setViolation(true)}>Наказание</button>
            </div>
          )}
      </div>
      <PlayerEdit
        playerData={playerData}
        user={user}
        selectedServer={selectedServer}
        name={name}
        setName={setName}
        discord={discord}
        setDiscord={setDiscord}
        role={role}
        setRole={setRole}
        balance={balance}
        setBalance={setBalance}
        birthday={birthday}
        setBirthday={setBirthday}
        modal={editPlayer}
        setModal={setEditPlayer}
        setResponseModal={setResponseModal}
        setResponseData={setResponseData}
        setStaff={setStaff}
      />
      <Vacation
        modal={vacation}
        setModal={setVacation}
        selectedServer={selectedServer}
        user={playerData}
      />
      <Violation
        modal={violation}
        setModal={setViolation}
        selectedServer={selectedServer}
        user={playerData}
        setStaff={setStaff}
      />
      <Modal visible={responseModal} setVisible={setResponseModal}>
        <h2 style={{ color: responseData["color"] }}>
          {responseData["content"]}
        </h2>
      </Modal>
    </div>
  );
}
