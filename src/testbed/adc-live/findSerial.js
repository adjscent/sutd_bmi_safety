const { SerialPort } = require("serialport");

async function findArduinoPort() {
  const ports = await SerialPort.list();

  // console.log("Available serial ports:");
  // ports.forEach((port) => {
  //   console.log(`- ${port.path} (${port.manufacturer || "Unknown"})`);
  // });

  // Patterns for common Arduino boards
  const arduinoPatterns = [
    /arduino/i,
    /usb serial/i,
    /usbserial/i,
    /wch/i,
    /ch340/i,
    /cp210x/i,
    /silicon labs/i,
    /ACM0/i,
    /Prolific/i,
  ];

  const port = ports.find((p) => {
    const info = `${p.path || ""} ${p.manufacturer || ""} ${p.friendlyName || ""} ${p.vendorId || ""} ${p.productId || ""}`;
    return arduinoPatterns.some((pattern) => pattern.test(info));
  });

  if (port) {
    console.log(`Found Arduino on port: ${port.path}`);
    return port.path;
  }

  throw new Error("Arduino serial port not found.");
}

module.exports = findArduinoPort;
