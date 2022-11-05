import React, { useState, useEffect, useContext } from "react";
import SelectServer from "../components/Selectors/SelectServer";
import Loader from "../components/Loader/Loader";
import "../styles/Activity.css";
import { Context } from "..";
import ActivityService from "../services/ActivityService";
import PlayerList from "../components/activity/PlayerList";
import ActivityData from "../components/activity/ActivityData";

export default function ActivityPage() {
  let server = "";
  const { store } = useContext(Context);
  const [date1, setDate1] = useState("");
  const [date2, setDate2] = useState("");
  const [players, setPlayers] = useState({});
  const [activity, setActivity] = useState({});
  const [activityPlayers, setActivityPlayers] = useState({});

  if (store.user["dt"]["lvl"] > 1 && store.user["tmrpg"]["lvl"] > 1) {
    server = "dt";
  } else {
    if (store.user["dt"]["lvl"] > 1) {
      server = "dt";
    } else if (store.user["tmrpg"]["lvl"] > 1) {
      server = "tmrpg";
    }
  }
  const [selectedServer, setSelectedServer] = useState(server);

  useEffect(() => {
    const setUsers = async () => {
      const response = await ActivityService.fetchPlayers();
      if (response) {
        setPlayers(response.data);
        setDate1(response.data["monday"]);
        setDate2(response.data[selectedServer]["lastDay"]);
      }
    };
    setUsers();
    document.title = "Игровая активность";
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    if (Object.keys(players).length > 0) {
      setActivityPlayers(players[selectedServer]["staff"]);
      setDate1(players["monday"]);
      setDate2(players[selectedServer]["lastDay"]);
    }
  }, [players, selectedServer]);

  useEffect(() => {
    const getActivity = async () => {
      const response = await ActivityService.fetchActivityPlayers(
        date1,
        date2,
        activityPlayers.map((player) => player.name),
        selectedServer
      );
      response && setActivity(response.data);
    };
    if (date1 && date2 && Object.keys(activityPlayers).length > 0) {
      getActivity();
    }
    // eslint-disable-next-line
  }, [activityPlayers, date1, date2]);

  if (Object.keys(activity).length === 0) {
    return <Loader />;
  }

  return (
    <div className="activityCheck">
      <div className="selectServer">
        {store.user["dt"]["lvl"] > 1 && store.user["tmrpg"]["lvl"] > 1 && (
          <SelectServer
            onChange={({ value }) => {
              setSelectedServer(value);
            }}
          />
        )}
      </div>
      <div className="activityData">
        <PlayerList
          date1={date1}
          date2={date2}
          setDate1={setDate1}
          setDate2={setDate2}
          players={players[selectedServer]["players"]}
          activityPlayers={activity}
          allData={activityPlayers}
          setData={setActivityPlayers}
          wipe={players[selectedServer]["wipe"]}
        />
        <div className="activityPlayersData">
          <ActivityData
            players={activityPlayers}
            data={activity}
            setData={setActivityPlayers}
          />
        </div>
      </div>
    </div>
  );
}
