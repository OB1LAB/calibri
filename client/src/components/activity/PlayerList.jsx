import { useState } from "react";
import Player from "./Player";
import classes from "./Activity.module.css";

export default function PlayerList({
  players,
  activityPlayers,
  date1,
  date2,
  setDate1,
  setDate2,
  wipe,
  setData,
  allData,
}) {
  const [find, setFind] = useState("");
  return (
    <div className={classes.players}>
      <div className={classes.dates}>
        <input
          value={date1}
          min={wipe}
          max={date2}
          onChange={(e) => setDate1(e.target.value)}
          type="date"
        />
        <input
          value={date2}
          min={wipe}
          max={date2}
          onChange={(e) => setDate2(e.target.value)}
          type="date"
        />
      </div>
      <div className={classes.find}>
        <input
          placeholder="Поиск..."
          value={find}
          onChange={(e) => setFind(e.target.value)}
        ></input>
      </div>
      <div className={classes.playerList}>
        {players
          .filter(
            (player) =>
              activityPlayers[player.name] === undefined &&
              player.name.toLowerCase().includes(find.toLowerCase())
          )
          .sort((a, b) => a.name.localeCompare(b.name))
          .sort((a, b) => b["lvl"] - a["lvl"])
          .slice(0, 25)
          .map((player, index) => {
            return (
              <Player
                key={player.name}
                player={player}
                setData={setData}
                allData={allData}
                index={index}
                act="add"
              />
            );
          })}
      </div>
    </div>
  );
}
