# face-mask-detection-raspberry-pi-project-


---

## Face Mask Detection System with Temperature Screening

An automated access control system built on Raspberry Pi that detects face masks via computer vision and performs temperature screening using thermal sensors.

### Hardware Components

| Component | Function |
| **Raspberry Pi 3** | Main controller & processing unit |
| **LM35** | Analog temperature sensor |
| **MCP3208** | 12-bit SPI ADC for sensor interfacing |
| **L293D** | DC motor driver for gate control |
| **LCD 16x2** | Status display (mask detection, temperature readings) |
| **UART/Serial** | Communication interface for mask detection input |

### System Workflow

1. **Mask Detection** — Receives detection signal via UART from external vision system
2. **Temperature Check** — Reads body temperature via LM35 through MCP3208 ADC
3. **Access Decision** — Opens gate (L293D motor driver) only if mask detected AND temperature is normal (90-100°F range)
4. **Real-time Feedback** — LCD displays mask status, temperature, and gate state

### Pin Configuration

| Device | GPIO Pins |
|--------|-----------|
| LCD RS, E, D4-D7 | 7, 11, 12, 13, 15, 16 |
| Motor Driver (L293D) | 29, 31 |
| SPI (MCP3208) | MOSI (19), MISO (21), SCLK (23), CE0 (24) |
| UART RX | Pin 10 |

### Software Requirements

```bash
pip install spidev RPi.GPIO
```

### Features

- ✅ Automated mask detection validation
- ✅ Contactless temperature screening
- ✅ Motor-controlled gate access
- ✅ Real-time LCD status updates
- ✅ SPI-based analog sensor reading
