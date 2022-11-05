import Player from "./Player";
import classes from "./Activity.module.css";

export default function ActivityData({ players, data, setData }) {
  return (
    <table className={classes.generalTable}>
      <thead>
        <tr>
          <td>Player</td>
          <td>[L]</td>
          <td>[G]</td>
          <td>[PM]</td>
          <td>[Warns]</td>
          <td>[Mutes]</td>
          <td>[Kicks]</td>
          <td>[Bans]</td>
          <td>[AVG]</td>
          <td>[Total]</td>
          <td>[Vanish]</td>
          <td>[Status]</td>
        </tr>
      </thead>
      <tbody>
        {players
          .sort((a, b) => a.name.localeCompare(b.name))
          .sort((a, b) => b["lvl"] - a["lvl"])
          .map((player, index) => {
            return data[player.name] !== undefined ? (
              <tr key={player.name}>
                <td>
                  <Player
                    player={player}
                    setData={setData}
                    act="delete"
                    allData={players}
                    index={index}
                  />
                </td>
                <td>{data[player.name]["L"]}</td>
                <td>{data[player.name]["G"]}</td>
                <td>{data[player.name]["PM"]}</td>
                <td>{data[player.name]["Warns"]}</td>
                <td>{data[player.name]["Mutes"]}</td>
                <td>{data[player.name]["Kicks"]}</td>
                <td>{data[player.name]["Bans"]}</td>
                <td>{data[player.name]["AVG"].replace("|", "</br>")}</td>
                <td>{data[player.name]["Total"]}</td>
                {data[player.name]["Vanish"] ? (
                  <td id="green">on</td>
                ) : (
                  <td id="red">off</td>
                )}
                {data[player.name]["Status"] ? (
                  <td id="green">online</td>
                ) : (
                  <td id="red">offline</td>
                )}
              </tr>
            ) : (
              <tr key={player.name}>
                <td>
                  <Player
                    player={player}
                    setData={setData}
                    act="delete"
                    allData={players}
                    index={index}
                  />
                </td>
                <td>?</td>
                <td>?</td>
                <td>?</td>
                <td>?</td>
                <td>?</td>
                <td>?</td>
                <td>?</td>
                <td>?</td>
                <td>?</td>
                <td id="red">?</td>
                <td id="red">?</td>
              </tr>
            );
          })}
      </tbody>
    </table>
  );
}
