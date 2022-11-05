import { useState } from "react";
import Player from "./Player";
import classes from "./Admin.module.css";
import PlayerAdd from "./PlayerAdd";
import Modal from "../modal/Modal";

export default function StaffList({
  staffData,
  user,
  selectedServer,
  setStaff,
}) {
  const [modal, setModal] = useState(false);
  const [responseModal, setResponseModal] = useState(false);
  const [responseData, setResponseData] = useState({
    color: "",
    content: "",
  });

  return (
    <div className={classes.staffList}>
      <button
        className={classes.addUser}
        onClick={() => {
          setModal(true);
        }}
      >
        Добавить состав
      </button>
      {staffData
        .filter((staff) => {
          return staff[selectedServer].lvl > 1;
        })
        .sort((a, b) => a.name.localeCompare(b.name))
        .sort((a, b) => b[selectedServer]["lvl"] - a[selectedServer]["lvl"])
        .map((staffPlayer) => {
          return (
            <Player
              key={staffPlayer.id}
              playerData={staffPlayer}
              user={user}
              selectedServer={selectedServer}
              setStaff={setStaff}
            />
          );
        })}
      <PlayerAdd
        user={user}
        selectedServer={selectedServer}
        modal={modal}
        setModal={setModal}
        setResponseData={setResponseData}
        setResponseModal={setResponseModal}
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
