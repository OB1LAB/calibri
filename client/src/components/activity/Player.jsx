import classes from "./Activity.module.css";

export default function StaffList({ allData, player, act, setData, index }) {
  return (
    <div>
      <button
        onClick={() => {
          if (act === "add") {
            !allData.includes(player) && setData([...allData, player]);
          } else {
            allData.splice(index, 1);
            setData([...allData]);
          }
        }}
        className={classes.player}
      >
        <img
          alt=""
          src={`https://skins.mcskill.net/?name=${player.name}&mode=5&fx=64&fy=64`}
        ></img>
        <h1 id={player.rank}>{player.name}</h1>
      </button>
    </div>
  );
}
