# Pet project to be created to test different components combined into one system

System diagram:

![System diagram](/shared-docs/images/esp32_nodered_mqtt_flutter_project.drawio.png)

***

## Quick description
The goal of the project is to create a room temperature control system. The system should be controlled via a Flutter application.

To avoid creating a physical environment, we emulate it. We take into account the dynamics of heat distribution in the room and from the heater to the sensor. All this is implemented on an ESP32 board.

Temperature control is implemented on Node-Red. It implements a PID algorithm. The parameters of the PID algorithm are set via MQTT messages from the user's application.
All of this is installed on an Oracle cloud server. Mosquitto MQTT broker is also installed there.

The user application is implemented on Flutter. This ensures its operation on different devices: Linux/Windows Desktop, Web page, Android, and iOS.
The application has a graphical chart for displaying temperature graphs. Text input fields are provided for the PID controller parameters. The user can also change the IP address of the MQTT broker.

The project is divided into the following parts:
- `ESP32` - implementation of the temperature control system emulator. Based on PlatformIO + Arduino ESP32 framework;
- `Node-Red` - implementation of the temperature controller. Based on Node-Red;
- `Flutter` - implementation of the user application. Based on Flutter;
- `Oracle VM` - Oracle Virtual Machine. The main database is Oracle Cloud Infrastructure Virtual Machine. The MQTT broker is also installed there.

***

## Quick setup (see detalis in [README.md](README.md))
- Install Oracle Cloud Infrastructure Virtual Machine;
- Install Mosquitto MQTT broker;    
- Install Node-Red;
- Upload ESP32 firmware;

***

## Quick start
- Run Oracle Cloud Infrastructure Virtual Machine;
  - Mosquitto MQTT broker runs on the VM;
- Run Node-Red (manually, there is issue to run it automatically); 
- ESP32 power on;
- Run Flutter application;

### Start in detalis:
In terminal run ssh connect to Oracle VM:
```
ssh oracle  
```

Then run Node-Red:
```
node-red
```

Then connect local browser to `http://localhost:1880/`. It will open the Node-Red web interface. Addionally open `http://localhost:1880/ui/` to open the Node-Red dashboard interface.

Web page screenshot:
![Web page screenshot](/shared-docs/images/node-red_preview.png)

Then run Flutter application:
- Open `/flutter-app/` directory in VSCode;
- run `/flutter-app/lib/main.dart` file. It will open the Flutter application;
  - if flutter folder copied for new place, then need to delete `/flutter-app/build` folder and run again;

Application page screenshot:
![Application screenshot](/shared-docs/images/flutter_app_preview.png)