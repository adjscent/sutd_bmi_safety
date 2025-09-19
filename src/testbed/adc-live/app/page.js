"use client";

import { useEffect, useRef, useState } from "react";
import io from "socket.io-client";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function Page() {
  const ch0Ref = useRef(null);
  const ch1Ref = useRef(null);
  const ch2Ref = useRef(null);
  const ch3Ref = useRef(null);
  const charts = [
    { ref: ch0Ref, name: "ch0" },
    { ref: ch1Ref, name: "ch1" },
    { ref: ch2Ref, name: "ch2" },
    { ref: ch3Ref, name: "ch3" },
  ];

  const [maxChannels, setMaxChannels] = useState(4); // Maximum number of channels in download
  const [maxY, setMaxY] = useState(500);
  const [minY, setMinY] = useState(-150);
  const socketRef = useRef();
  const [action, setAction] = useState("nothing");
  const [extraFilename, setExtraFilename] = useState("");
  const [duration, setDuration] = useState(1);
  const [paused, setPaused] = useState(false);
  const [showNotification, setShowNotification] = useState(false);
  const [dataPoints, setDataPoints] = useState(() => {
    const now = Date.now();
    return Array.from({ length: duration }, (_, i) => ({
      timestamp: now - (duration - 1 - i) * 1000,
      ch0: { a: 0, e: 0 },
      ch1: { a: 0, e: 0 },
      ch2: { a: 0, e: 0 },
      ch3: { a: 0, e: 0 },
    }));
  });

  useEffect(() => {
    socketRef.current = io();
    const socket = socketRef.current;
    socket.on("adc_data", (d) => {
      if (paused) return;
      const entry = { timestamp: Date.now(), ...d };
      setDataPoints((prev) => {
        const cutoff = Date.now() - duration * 1000;
        return [entry, ...prev].filter((x) => x.timestamp >= cutoff);
      });
    });
    return () => socket.disconnect();
  }, [paused, duration]);

  const labels = dataPoints.map((d) =>
    new Date(d.timestamp).toLocaleTimeString("en-SG", {
      hour12: false,
      minute: "2-digit",
      second: "2-digit",
      fractionalSecondDigits: 3,
    })
  );

  const commonOptions = {
    animation: false,
    scales: {
      x: { title: { display: true, text: "Time" } },
      y: {
        min: minY,
        max: maxY,
        ticks: { stepSize: 5 },
        title: { display: true, text: "Value" },
      },
    },
    plugins: { legend: { position: "top" } },
  };

  const chartDataCh0 = {
    labels,
    datasets: [
      {
        label: "Channel 0 Activation",
        data: dataPoints.map((dp) => dp.ch0?.a || 0),
        borderColor: "red",
      },
      {
        label: "Channel 0 Envelope",
        data: dataPoints.map((dp) => dp.ch0?.e || 0),
        borderColor: "pink",
      },
    ],
  };

  const chartDataCh1 = {
    labels,
    datasets: [
      {
        label: "Channel 1 Activation",
        data: dataPoints.map((dp) => dp.ch1?.a || 0),
        borderColor: "green",
      },
      {
        label: "Channel 1 Envelope",
        data: dataPoints.map((dp) => dp.ch1?.e || 0),
        borderColor: "lightgreen",
      },
    ],
  };

  const chartDataCh2 = {
    labels,
    datasets: [
      {
        label: "Channel 2 Activation",
        data: dataPoints.map((dp) => dp.ch2?.a || 0),
        borderColor: "blue",
      },
      {
        label: "Channel 2 Envelope",
        data: dataPoints.map((dp) => dp.ch2?.e || 0),
        borderColor: "lightblue",
      },
    ],
  };

  const chartDataCh3 = {
    labels,
    datasets: [
      {
        label: "Channel 3 Activation",
        data: dataPoints.map((dp) => dp.ch3?.a || 0),
        borderColor: "brown",
      },
      {
        label: "Channel 3 Envelope",
        data: dataPoints.map((dp) => dp.ch3?.e || 0),
        borderColor: "black",
      },
    ],
  };

  const createActionFilename = (action, extra) => {
    if (!extra) return action;
    return `${action}_${extra}`;
  };

  const downloadAll = () => {
    const now = Date.now();
    // CSV
    // Build CSV header and rows based on maxChannels
    const channelHeaders = [];
    for (let i = 0; i < maxChannels; i++) {
      channelHeaders.push(`Ch${i} Act`, `Ch${i} Env`);
    }
    channelHeaders.push("Action");

    const rows = [
      ["Timestamp", ...channelHeaders],
      ...dataPoints.map((d) => {
        const row = [new Date(d.timestamp).toISOString()];
        for (let i = 0; i < maxChannels; i++) {
          row.push(d[`ch${i}`]?.a || 0, d[`ch${i}`]?.e || 0);
        }
        row.push(createActionFilename(action, extraFilename));
        return row;
      }),
    ];
    const csv = rows.map((r) => r.join(",")).join("\n");
    const csvBlob = new Blob([csv], { type: "text/csv" });
    const csvUrl = URL.createObjectURL(csvBlob);
    const csvLink = document.createElement("a");
    csvLink.href = csvUrl;
    csvLink.download = `${now}_${createActionFilename(
      action,
      extraFilename
    )}_adc.csv`;
    csvLink.click();

    charts.slice(0, maxChannels).forEach(({ ref, name }) => {
      if (ref.current) {
        const url = ref.current.toBase64Image();
        const a = document.createElement("a");
        a.href = url;
        a.download = `${now}_${createActionFilename(
          action,
          extraFilename
        )}_${name}.png`;
        a.click();
      }
    });
  };

  const downloadLater = async () => {
    await new Promise((res) => setTimeout(res, duration)); // Wait another 5s
    downloadAll(); // Trigger CSV + PNGs

    // Show notification
    setShowNotification(true);
    setTimeout(() => setShowNotification(false), 3000);
  };

  return (
    <main style={{ width: "90%", margin: "1rem auto" }}>
      {showNotification && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            background: "#4caf50",
            color: "white",
            textAlign: "center",
            zIndex: 9999,
          }}
        >
          ✅ All files downloaded.
        </div>
      )}

      <h2>Live ADC (last {duration}s)</h2>
      <div style={{ marginBottom: 16, marginTop: 16 }}>
        <label>
          Window (s):
          <input
            type="number"
            min="1"
            max="10"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            style={{ width: 50, marginLeft: 8 }}
          />
        </label>
        <button onClick={() => setPaused((p) => !p)} style={{ marginLeft: 16 }}>
          {paused ? "Resume" : "Pause"}
        </button>
        <button onClick={downloadAll} style={{ marginLeft: 16 }}>
          Download CSV + PNGs
        </button>
        <button onClick={downloadLater} style={{ marginLeft: 16 }}>
          Download All after {duration}s
        </button>
        <label style={{ marginLeft: 16 }}>
          Filename:
          <select
            value={action}
            onChange={(e) => setAction(e.target.value)}
            style={{ width: 100, marginLeft: 8 }}
          >
            <option value="disconnected">disconnected</option>
            <option value="nothing">nothing</option>
            <option value="supination">supination</option>
            <option value="flexion">flexion</option>
            <option value="grasp">grasp</option>
            <option value="pronation">pronation</option>
            <option value="extension">extension</option>
            <option value="open">open</option>
            <option value="left">left</option>
            <option value="right">right</option>
          </select>
        </label>
        <label style={{ marginLeft: 16 }}>
          Extra:
          <input
            value={extraFilename}
            onChange={(e) => setExtraFilename(e.target.value)}
            style={{ width: 100, marginLeft: 8 }}
          ></input>
        </label>
        <label style={{ marginLeft: 16 }}>
          Max Channels:
          <input
            type="number"
            min="1"
            max="4"
            value={maxChannels}
            onChange={(e) => setMaxChannels(e.target.value)}
            style={{ width: 30, marginLeft: 8 }}
          ></input>
        </label>
        <label style={{ marginLeft: 16 }}>
          Max Y:
          <input
            type="number"
            step="10"
            value={maxY}
            onChange={(e) => setMaxY(e.target.value)}
            style={{ width: 50, marginLeft: 8 }}
          />
        </label>
        <label style={{ marginLeft: 16 }}>
          Min Y:
          <input
            type="number"
            step="10"
            value={minY}
            onChange={(e) => setMinY(e.target.value)}
            style={{ width: 50, marginLeft: 8 }}
          />
        </label>
      </div>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "1rem",
          justifyContent: "space-between",
        }}
      >
        <div style={{ flex: "1 1 100%" }}>
          <h3 style={{ textAlign: "center" }}>Channel 0</h3>
          <Line ref={ch0Ref} data={chartDataCh0} options={commonOptions} />
        </div>
        <div style={{ flex: "1 1 100%" }}>
          <h3 style={{ textAlign: "center" }}>Channel 1</h3>
          <Line ref={ch1Ref} data={chartDataCh1} options={commonOptions} />
        </div>
        <div style={{ flex: "1 1 100%" }}>
          <h3 style={{ textAlign: "center" }}>Channel 2</h3>
          <Line ref={ch2Ref} data={chartDataCh2} options={commonOptions} />
        </div>
        <div style={{ flex: "1 1 100%" }}>
          <h3 style={{ textAlign: "center" }}>Channel 3</h3>
          <Line ref={ch3Ref} data={chartDataCh3} options={commonOptions} />
        </div>
      </div>
    </main>
  );
}
