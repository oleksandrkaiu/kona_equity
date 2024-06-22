import Chart from "chart.js";

function init() {
  for (let chartInfoEl of document.querySelectorAll(".chart-info")) {
    const canvas = chartInfoEl.querySelector(".chart-info__canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    const labels =
      "2019 Q2,2019 Q3,2019 Q4,2020 Q1,2020 Q2,2020 Q3,2020 Q4,2021 Q1,2021 Q2".split(
        ","
      );
    const data =
      "2400000,2400000,2171000,2171000,2171000,2171000,2171000,3003000,3003000"
        .split(",")
        .map((i) => parseInt(i));

    function abbreviate_number(num) {
      if (num === null) return null;
      if (num === 0) return "0";

      const fixed = 2;
      const b = num.toPrecision(2).split("e");
      const k =
        b.length === 1 ? 0 : Math.floor(Math.min(b[1].slice(1), 14) / 3);
      const c =
        k < 1
          ? num.toFixed(0 + fixed)
          : (num / Math.pow(10, k * 3)).toFixed(1 + fixed);
      const d = c < 0 ? c : Math.abs(c);
      const e = d + " " + ["", "K", "M", "B", "T"][k];

      return e;
    }

    const chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Revenue",
            backgroundColor: "#00D1C1",
            borderColor: "#00D1C1",
            data: data,
            fill: false,
          },
        ],
      },
      options: {
        layout: {
          padding: {
            top: 5,
            left: 5,
            right: 5,
            bottom: 10,
          },
        },
        legend: {
          display: false,
        },
        responsive: true,
        tooltips: {
          mode: "index",
          intersect: false,
          callbacks: {
            label: function (tooltipItem, data) {
              let label = data.datasets[tooltipItem.datasetIndex].label || "";

              if (label) {
                label += ": ";
              }
              label += abbreviate_number(tooltipItem.yLabel);
              return label;
            },
          },
        },
        hover: {
          mode: "nearest",
          intersect: true,
        },
        scales: {
          xAxes: [
            {
              gridLines: {
                display: false,
              },
              display: true,
              scaleLabel: {
                display: true,
                labelString: "Quarter",
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: false,
              },
              display: false,
              scaleLabel: {
                display: true,
                labelString: "Revenue",
              },
            },
          ],
        },
      },
    });
  }
}

if (["interactive", "complete"].includes(document.readyState)) {
  init();
} else {
  window.addEventListener("DOMContentLoaded", init);
}
