import "chart.js/auto";
import { Bar } from "react-chartjs-2";

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
        stepSize: 50,
      },
    },
  },
  maintainAspectRatio: false,
};

export default function ChartStaff({ data }) {
  const dataBar = {
    labels: data.labels,
    datasets: [
      {
        indexAxis: "x",
        label: "Итог за неделю",
        data: data.playerData,
        backgroundColor: [
          "rgba(255, 26, 104, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
        ],
        borderColor: [
          "rgba(255, 26, 104, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };
  return (
    <div style={{ height: "600px", width: "100%" }}>
      <Bar height="200px" width="200px" data={dataBar} options={options} />
    </div>
  );
}
