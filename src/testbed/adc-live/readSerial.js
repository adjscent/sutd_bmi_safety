const { SerialPort } = require("serialport");
const { ReadlineParser } = require("@serialport/parser-readline");

function tryParseInt(value, base) {
  const parsed = parseInt(value, base);
  return isNaN(parsed) ? 0 : parsed;
}

module.exports = function connect(io, portPath) {
  const port = new SerialPort({
    path: portPath,
    baudRate: 115200,
  });
  const parser = port.pipe(new ReadlineParser({ delimiter: "\n" }));

  console.log("CONNECT");
  parser.on("data", (line) => {
    const parts = line
      .trim()
      .split(",")
      .map((s) => tryParseInt(s, 10));
    const adc_data = {};

    for (let i = 0; i < parts.length; i += 2) {
      adc_data[`ch${i / 2}`] = { a: parts[i], e: parts[i + 1] };
    }

    io.emit("adc_data", adc_data);
  });

  port.on("error", (err) => {
    console.error("Serial error:", err);
    console.log("INITIATING RECONNECT");
    setTimeout(function () {
      console.log("RECONNECTING TO ARDUINO");
      connect(io, portPath);
    }, 2000);
  });
  port.on("close", (err) => {
    console.error("Serial error:", err);
    console.log("INITIATING RECONNECT");
    setTimeout(function () {
      console.log("RECONNECTING TO ARDUINO");
      connect(io, portPath);
    }, 2000);
  });
};
