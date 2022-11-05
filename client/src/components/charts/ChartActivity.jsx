import "chart.js/auto";
import { Bar } from "react-chartjs-2";

const colors = [
  "rgba(255, 0, 0, 0.5)",
  "rgba(255, 128, 0, 0.5)",
  "rgba(128, 255, 0, 0.5)",
  "rgba(128, 0, 255, 0.5)",
  "rgba(255, 0, 128, 0.5)",
];

const options = {
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    y: {
      title: {
        display: true,
        text: "Value",
      },
      ticks: {
        stepSize: 1,
      },
    },
  },
  maintainAspectRatio: false,
};

export default function ChartActivity({ data }) {
  const getData = () => {
    let playerData = [];
    let colorIndex = 0;
    for (let player in data.playerData) {
      if (colorIndex > colors.length) {
        colorIndex = 0;
      }
      let color = {
        backgroundColor: colors[colorIndex],
        borderWidth: 1,
      };
      playerData.push({ ...data.playerData[player], ...color });
      colorIndex += 1;
    }
    return playerData;
  };

  const dataHorBar = {
    labels: data.labels,
    datasets: getData(),
  };
  return (
    <div style={{ height: "600px", width: "100%" }}>
      <Bar height="200px" width="200px" data={dataHorBar} options={options} />
    </div>
  );
}
