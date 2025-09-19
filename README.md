# Releases
* 1.0 - Initial release:
  - Node-Red Threshold node only
  - ESP32 sensor data emulated by random generator
  - Flutter: see: `flutter_application_1` separate project folder
  - Oracle VM setup done

* 2.0 
  - Node-Red used for http GET request for ESP32 parameters
  - ESP32 dynamic emulator for "room with heater and sensor"
  - Node-Red uses simple tempetature controller

* 3.0 
  - Python scritp to monitor and plot data (plotting.py with performance issue and plotAnimate.py with no issues)


* 4.0
  - Main code still the same, PID example added for learning
  
* 5.0
  - PID control added to Node-Red, flogging setup added
  
* 5.1 
  - PID parameters from inject nde fixed, and from MQTT topic added

* 6.0
  - Flutter first app test added - see folder `flutter` here. Temperature Graphic works
  - Note: Flutter app works from different project, there dart code only. Tested as Linux app.

* 6.1
  - Flutter UI many improvements and bug fixes

* 6.2
  - Flutter UI some fixes - remove current tempetature bar and setpoint update bar
  - MQTT setpoint fixed, works now

* 7.0
  - Flutter Chart fixed, Node-Red PID parameters fixed
  - ESP32 Push Button start/stop added


***

### Python plotting run:
- First install venv only once:
```
python3 -m venv .venv
pip-compile requirements.in
python3 -m pip install -r requirements.txt
```

Then run:
```
cd src
. activate
python plotAnimate.py
```

***

# Oracle VM connect:
ssh oracle

## Node-Red install and setup
- Via nvm (Node Version Manager)
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
source ~/.bashrc
nvm install --lts

node --version
v22.18.0

npm --version
10.9.3
```

Oracle VM setup:
Security List in Oracle Cloud:
GotoOracle Cloud Console → Networking → Virtual Cloud Networks → VCNxxx → Security Lists 
add Ingress rule:
```
Source CIDR: 0.0.0.0/0
IP Protocol: TCP
Destination Port Range: 1880
```
Note: `Serurity List` should be added to `Subnet`

Firewall setup:
```
sudo firewall-cmd --permanent --add-port=1880/tcp
sudo firewall-cmd --reload
```

# Mosquitto install and setup
Install from source (binary install failed for Oracle VM): 

Nessarry libs:
```
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y cmake gcc gcc-c++ make c-ares-devel libuuid-devel libwebsockets-devel openssl-devel
```
Proper script (may not work if not some libs are missing):
wget https://mosquitto.org/files/source/mosquitto-2.0.18.tar.gz
tar xvf mosquitto-2.0.18.tar.gz
cd mosquitto-2.0.18
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

Additional libs install:
```
sudo dnf install -y cmake gcc gcc-c++ make

sudo dnf install -y openssl-devel
```

Additional lib `libwebsockets` install from source:
```
wget https://github.com/warmcat/libwebsockets/archive/refs/tags/v4.3.3.tar.gz
tar -xzf v4.3.3.tar.gz
cd libwebsockets-4.3.3
mkdir build && cd build

# make it:
cmake .. -DCMAKE_BUILD_TYPE=Release -DLWS_WITH_SSL=ON
make -j$(nproc)
sudo make install
sudo ldconfig
```

Then from folder: `mosquitto-2.0.18/build`:
```
rm -rf *
cmake ..
make -j$(nproc)
sudo make install
```

## Mosquitto access setup
Add in `/usr/local/etc/mosquitto/mosquitto.conf`:
```
nginx
listener 1883 0.0.0.0
allow_anonymous true
```

Oracle VM firewall for Mosquitto:
```
sudo firewall-cmd --add-port=1883/tcp --permanent
sudo firewall-cmd --reload
```

Mosquitto test:

One terminal:
```
mosquitto_sub -h localhost -t test/topic
```

Second terminal:
```
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
```

Option from remote PC terminal:
```
mosquitto_pub -h <IP_VM> -p 1883 -t test/topic -m "Hi from outside"
```

If errors (it actual was):
Libraries cash update:
```
sudo sh -c "echo /usr/local/lib >> /etc/ld.so.conf.d/mosquitto.conf
sudo ldconfig
```

Check:
```
ldconfig -p | grep libmosquitto
```

Possible error (libmosquitto path not found):
```
sudo find /usr/local -name "libmosquitto.so*"
```
My output:
```
[opc@instance-20250809-1749 ~]$ sudo find /usr/local -name "libmosquitto.so*"
/usr/local/lib64/libmosquitto.so.2.0.18
/usr/local/lib64/libmosquitto.so.1
/usr/local/lib64/libmosquitto.so
[opc@instance-20250809-1749 ~]$ sudo find /usr/local -name "libmosquitto.so*"
/usr/local/lib64/libmosquitto.so.2.0.18
/usr/local/lib64/libmosquitto.so.1
/usr/local/lib64/libmosquitto.so
```

So need add path:
```
echo "/usr/local/lib64" | sudo tee /etc/ld.so.conf.d/mosquitto.conf
sudo ldconfig
```
Then good result:
```
ldconfig -p | grep libmosquitto
 ldconfig -p | grep libmosquitto >> у меня! есть!
	libmosquittopp.so.1 (libc6,x86-64) => /usr/local/lib64/libmosquittopp.so.1
	libmosquittopp.so (libc6,x86-64) => /usr/local/lib64/libmosquittopp.so
	libmosquitto.so.1 (libc6,x86-64) => /usr/local/lib64/libmosquitto.so.1
	libmosquitto.so (libc6,x86-64) => /usr/local/lib64/libmosquitto.so
```

Then Oracle VM setup:
Security List in Oracle Cloud:
GotoOracle Cloud Console → Networking → Virtual Cloud Networks → VCNxxx → Security Lists 
add Ingress rule:
```
Source CIDR: 0.0.0.0/0
IP Protocol: TCP
Destination Port Range: 1883
```
Note: `Serurity List` should be added to `Subnet`

Firewall setup:
```
sudo firewall-cmd --permanent --add-port=1883/tcp
sudo firewall-cmd --reload
```

## Mosquitto last setup steps:
`mosquitto.conf` setup path:

`/etc/mosquitto/mosquitto.conf`
or
`/usr/local/etc/mosquitto/mosquitto.conf`


`mosquitto.conf` edit:
```
listener 1883
allow_anonymous true
```

Mosquitto restart:
```
sudo pkill mosquitto
mosquitto -c /etc/mosquitto/mosquitto.conf
```
And test from remote PC again:
```
mosquitto_pub -h 130.61.123.45 -t test/topic -m "hello"
mosquitto_sub -h 130.61.123.45 -t test/topic
```


***

# How to setup Oracle VM ssh key access at remote PC:
`~/.ssh/config`:
```
Host 130.61.123.45
    User opc
    IdentityFile ~/.ssh/ssh-key-2025-08-09.key
    IdentitiesOnly yes
```