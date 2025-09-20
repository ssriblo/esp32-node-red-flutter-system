import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/services.dart';

/// ====== НАСТРОЙКИ ПОД ТВОЮ VM ======
const String kBrokerHost = '130.61.123.45'; // IP Oracle VM с Mosquitto
const int kBrokerPort = 1883;               // незашифрованный MQTT
const String kClientId  = 'flutter_client_01';

const String kTopicSensors = 'esp32/sensors'; // JSON: {"temp": 28.5, "hum": 60}
const String kTopicPidParams = 'node_red/pid_parameters'; // Тема для отправки PID-параметров
const String kTopicSetpoint = 'node_red/setpoint'; // Тема для отправки уставки температуры

/// ====== МОДЕЛЬ ТОЧКИ ГРАФИКА ======
class TempPoint {
  final DateTime t;
  final double value;
  TempPoint(this.t, this.value);
}

/// ====== MQTT СЕРВИС ======
class MqttService {
  late MqttServerClient client;
  final void Function(Map<String, dynamic> json) onSensorJson;

  MqttService({
  required this.onSensorJson,
  }) {
  client = MqttServerClient(kBrokerHost, kClientId)
    ..port = kBrokerPort
    ..keepAlivePeriod = 30
    ..autoReconnect = true
    ..onConnected = _onConnected
    ..onDisconnected = _onDisconnected
    ..resubscribeOnAutoReconnect = true
    ..logging(on: false);
  }

  Future<void> connect() async {
  final connMess = MqttConnectMessage()
      .withClientIdentifier(kClientId)
      .startClean(); // без сохранённой сессии

  client.connectionMessage = connMess;

  try {
    await client.connect(); // без логина/пароля (allow_anonymous true)
  } catch (_) {
    client.disconnect();
    rethrow;
  }

  client.updates?.listen((events) {
    // events — список полученных сообщений за "тик"
    for (final e in events) {
      final recMess = e.payload as MqttPublishMessage;
      final topic = e.topic;
      final payload =
          MqttPublishPayload.bytesToStringAsString(recMess.payload.message);

      if (topic == kTopicSensors) {
        try {
          final jsonMap = jsonDecode(payload) as Map<String, dynamic>;
          onSensorJson(jsonMap);
        } catch (_) {
          // игнорируем битые payload'ы
        }
      }
    }
  });
  }

  void _onConnected() {
  client.subscribe(kTopicSensors, MqttQos.atMostOnce);
  }

  void _onDisconnected() {
  // можно показать тост/баннер в UI через колбэки, если нужно
  }

  void dispose() {
  client.disconnect();
  }

  void sendPidParameters(double p, double i, double d) {
  final pidData = {
    'p': p,
    'i': i,
    'd': d,
  };

  final message = jsonEncode(pidData);
  final builder = MqttClientPayloadBuilder();
  builder.addString(message);

  client.publishMessage(
    kTopicPidParams,
    MqttQos.atMostOnce,
    builder.payload!,
  );
  }

  void sendSetpoint(double setpoint) {
  final setpointData = {
    'setpoint': setpoint,
  };

  final message = jsonEncode(setpointData);
  final builder = MqttClientPayloadBuilder();
  builder.addString(message);

  client.publishMessage(
    kTopicSetpoint,
    MqttQos.atMostOnce,
    builder.payload!,
  );
  }
}

/// ====== ПРИЛОЖЕНИЕ ======
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
  return MaterialApp(
    title: 'ESP32 Monitor',
    theme: ThemeData(
      colorSchemeSeed: Colors.indigo,
      useMaterial3: true,
    ),
    home: const DashboardPage(),
    debugShowCheckedModeBanner: false,
  );
  }
}

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});
  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  late final MqttService _mqtt;
  final List<TempPoint> _points = <TempPoint>[];
  double? _lastTemp;
  double? _lastHum;
  bool _isConnected = false;
  double _setpoint = 22.0; // Начальное значение уставки температуры

  static const int _maxPoints = 300; // Максимум точек на графике

  final TextEditingController _pController = TextEditingController(text: '0.1');
  final TextEditingController _iController = TextEditingController(text: '0.1');
  final TextEditingController _dController = TextEditingController(text: '0.1');

  @override
  void initState() {
  super.initState();
  _mqtt = MqttService(
    onSensorJson: (json) {
      final now = DateTime.now();
      final temp = (json['temp'] as num?)?.toDouble();
      final hum  = (json['hum']  as num?)?.toDouble();
      if (temp != null) {
        setState(() {
          _lastTemp = temp;
          _points.add(TempPoint(now, temp));
          if (_points.length > _maxPoints) {
            _points.removeAt(0);
          }
        });
      }
      if (hum != null) {
        setState(() => _lastHum = hum);
      }
    },
  );

  _connectMqtt();
  }

  Future<void> _connectMqtt() async {
  try {
    await _mqtt.connect();
    setState(() => _isConnected = true);
  } catch (e) {
    setState(() => _isConnected = false);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('MQTT connect error: $e')),
      );
    }
  }
  }

  @override
  void dispose() {
  _mqtt.dispose();
  _pController.dispose();
  _iController.dispose();
  _dController.dispose();
  super.dispose();
  }

  Future<void> _sendPidParameters() async {
  final p = double.tryParse(_pController.text);
  final i = double.tryParse(_iController.text);
  final d = double.tryParse(_dController.text);

  if (p == null || i == null || d == null) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Invalid PID values')),
    );
    return;
  }

  _mqtt.sendPidParameters(p, i, d);
  
  // Show success feedback
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text('PID parameters sent: P=$p, I=$i, D=$d'),
      backgroundColor: Colors.green,
    ),
  );
  }

  void _onSetpointChanged(double value) {
  setState(() {
    _setpoint = value;
  });
  _mqtt.sendSetpoint(value);
  
  // Show feedback
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text('Setpoint changed to: ${value.toStringAsFixed(1)}°C'),
      backgroundColor: Colors.blue,
      duration: const Duration(seconds: 1),
    ),
  );
  }

  @override
  Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(
      title: const Text('ESP32 — Temperature Monitor'),
      backgroundColor: Colors.indigo,
      foregroundColor: Colors.white,
      actions: [
        // Connection status indicator
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          child: Row(
            children: [
              Icon(
                _isConnected ? Icons.wifi : Icons.wifi_off,
                color: _isConnected ? Colors.green : Colors.red,
              ),
              const SizedBox(width: 8),
              // Temperature and humidity display
              _buildSensorDisplay(
                icon: Icons.thermostat,
                value: _lastTemp,
                unit: '°C',
                formatter: (v) => v.toStringAsFixed(1),
              ),
              const SizedBox(width: 16),
              _buildSensorDisplay(
                icon: Icles.water_drop,
                value: _lastHum,
                unit: '%',
                formatter: (v) => v.toStringAsFixed(0),
              ),
            ],
          ),
        )
      ],
    ),
    body: Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            Colors.indigo.shade50,
            Colors.white,
          ],
        ),
      ),
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _TempChart(points: _points),
          const SizedBox(height: 20),
          _SetpointSlider(
            setpoint: _setpoint,
            onChanged: _onSetpointChanged,
            currentTemp: _lastTemp,
          ),
          const SizedBox(height: 20),
          _PidControls(
            pController: _pController,
            iController: _iController,
            dController: _dController,
            onSend: _sendPidParameters,
          ),
          const SizedBox(height: 16),
          _ConnectionInfo(
            isConnected: _isConnected,
            brokerHost: kBrokerHost,
            brokerPort: kBrokerPort,
            topicSensors: kTopicSensors,
            topicPidParams: kTopicPidParams,
            topicSetpoint: kTopicSetpoint,
          ),
        ],
      ),
    ),
  );
  }

  Widget _buildSensorDisplay({
  required IconData icon,
  required double? value,
  required String unit,
  required String Function(double) formatter,
  }) {
  return Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Icon(icon, size: 18, color: Colors.white70),
      const SizedBox(width: 4),
      Text(
        value != null ? '${formatter(value)}$unit' : '—',
        style: const TextStyle(
          color: Colors.white,
          fontSize: 14,
          fontWeight: FontWeight.w500,
        ),
      ),
    ],
  );
  }
}

class _TempChart extends StatelessWidget {
  final List<TempPoint> points;
  const _TempChart({required this.points});

  @override
  Widget build(BuildContext context) {
  if (points.isEmpty) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        height: 300,
        padding: const EdgeInsets.all(16),
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.show_chart, size: 48, color: Colors.grey),
              SizedBox(height: 8),
              Text(
                'Waiting for temperature data...',
                style: TextStyle(color: Colors.grey),
              ),
            ],
          ),
        ),
      ),
    );
  }

  final spots = points
      .map((p) => FlSpot(p.t.millisecondsSinceEpoch.toDouble(), p.value))
      .toList();

  final minX = spots.isNotEmpty ? spots.first.x : 0.0;
  final maxX = spots.isNotEmpty ? spots.last.x : 0.0;
  final minY = spots.isNotEmpty
      ? spots.map((e) => e.y).reduce((a, b) => a < b ? a : b)
      : 0.0;
  final maxY = spots.isNotEmpty
      ? spots.map((e) => e.y).reduce((a, b) => a > b ? a : b)
      : 0.0;

  final yInterval = (maxY - minY) / 5 == 0 ? 1.0 : (maxY - minY) / 5;

  return Card(
    elevation: 4,
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
    child: Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.analytics, color: Colors.indigo),
              const SizedBox(width: 8),
              const Text(
                'Temperature Chart',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.indigo,
                ),
              ),
              const Spacer(),
              Text(
                '${points.length} points',
                style: const TextStyle(
                  color: Colors.grey,
                  fontSize: 12,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          AspectRatio(
            aspectRatio: 1.7,
            child: LineChart(
              LineChartData(
                minX: minX,
                maxX: maxX,
                minY: minY - yInterval,
                maxY: maxY + yInterval,
                gridData: FlGridData(
                  show: true,
                  drawHorizontalLine: true,
                  horizontalInterval: yInterval,
                  getDrawingHorizontalLine: (value) => FlLine(
                    color: Colors.grey.withOpacity(0.3),
                    strokeWidth: 1,
                  ),
                ),
                titlesData: FlTitlesData(
                  topTitles: AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                  rightTitles: AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                  leftTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      interval: yInterval,
                      reservedSize: 40,
                      getTitlesWidget: (value, meta) {
                        final text = value.toStringAsFixed(2);
                        return SideTitleWidget(
                          axisSide: meta.axisSide,
                          child: Text(
                            text,
                            style: const TextStyle(
                              fontSize: 10,
                              color: Colors.grey,
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                  bottomTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 30,
                      interval: (maxX - minX) / 4 == 0 ? 1.0 : (maxX - minX) / 4,
                      getTitlesWidget: (value, meta) {
                        final dt = DateTime.fromMillisecondsSinceEpoch(value.toInt());
                        return Text(
                          '${dt.hour}:${dt.minute.toString().padLeft(2, '0')}',
                          style: const TextStyle(
                            fontSize: 10,
                            color: Colors.grey,
                          ),
                        );
                      },
                    ),
                  ),
                ),
                borderData: FlBorderData(
                  show: true,
                  border: Border.all(
                    color: Colors.grey.withOpacity(0.3),
                    width: 1,
                  ),
                ),
                lineBarsData: [
                  LineChartBarData(
                    spots: spots,
                    isCurved: true,
                    color: Colors.indigo,
                    barWidth: 3,
                    shadow: const Shadow(
                      color: Colors.indigo,
                      blurRadius: 8,
                      offset: Offset(0, 2),
                    ),
                    dotData: FlDotData(show: false),
                    belowBarData: BarAreaData(
                      show: true,
                      gradient: LinearGradient(
                        colors: [
                          Colors.indigo.withOpacity(0.3),
                          Colors.indigo.withOpacity(0.1),
                        ],
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                      ),
                    ),
                    gradient: LinearGradient(
                      colors: [
                        Colors.indigo.shade400,
                        Colors.indigo.shade300,
                      ],
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    ),
  );
  }
}

class _SetpointSlider extends StatelessWidget {
  final double setpoint;
  final Function(double) onChanged;
  final double? currentTemp;

  const _SetpointSlider({
  required this.setpoint,
  required this.onChanged,
  this.currentTemp,
  });

  @override
  Widget build(BuildContext context) {
  return Card(
    elevation: 4,
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
    child: Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.thermostat, color: Colors.orange),
              const SizedBox(width: 8),
              const Text(
                'Temperature Setpoint',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.orange,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              const Icon(Icons.arrow_downward, size: 20, color: Colors.grey),
              const SizedBox(width: 4),
              const Text(
                '10°C',
                style: TextStyle(fontSize: 12, color: Colors.grey),
              ),
              Expanded(
                child: Slider(
                  value: setpoint,
                  min: 10.0,
                  max: 35.0,
                  divisions: 25, // 1°C steps
                  label: '${setpoint.toStringAsFixed(1)}°C',
                  onChanged: onChanged,
                  activeColor: Colors.orange,
                  inactiveColor: Colors.orange.shade200,
                ),
              ),
              const Icon(Icons.arrow_upward, size: 20, color: Colors.grey),
              const SizedBox(width: 4),
              const Text(
                '35°C',
                style: TextStyle(fontSize: 12, color: Colors.grey),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Setpoint: ${setpoint.toStringAsFixed(1)}°C',
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  color: Colors.orange,
                ),
              ),
              if (currentTemp != null)
                Text(
                  'Current: ${currentTemp!.toStringAsFixed(1)}°C',
                  style: const TextStyle(
                    color: Colors.blue,
                    fontWeight: FontWeight.w500,
                  ),
                ),
            ],
          ),
        ],
      ),
    ),
  );
  }
}

class _PidControls extends StatelessWidget {
  final TextEditingController pController;
  final TextEditingController iController;
  final TextEditingController dController;
  final Future<void> Function() onSend;

  const _PidControls({
  required this.pController,
  required this.iController,
  required this.dController,
  required this.onSend,
  });

  @override
  Widget build(BuildContext context) {
  return Card(
    elevation: 4,
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
    child: Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.tune, color: Colors.indigo),
              const SizedBox(width: 8),
              const Text(
                'PID Parameters Control',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.indigo,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Text(
            'Adjust the PID parameters for temperature control:',
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              _buildPidField(label: 'Proportional (P)', controller: pController),
              const SizedBox(width: 12),
              _buildPidField(label: 'Integral (I)', controller: iController),
              const SizedBox(width: 12),
              _buildPidField(label: 'Derivative (D)', controller: dController),
              const SizedBox(width: 16),
              ElevatedButton.icon(
                onPressed: onSend,
                icon: const Icon(Icons.send),
                label: const Text('Send Parameters'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                ),
              ),
            ],
          ),
        ],
      ),
    ),
  );
  }

  Widget _buildPidField({
  required String label,
  required TextEditingController controller,
  }) {
  return SizedBox(
    width: 80, // Fixed width for 7 symbols
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w500,
            color: Colors.grey,
          ),
        ),
        const SizedBox(height: 4),
        TextField(
          controller: controller,
          decoration: InputDecoration(
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: const BorderSide(color: Colors.grey),
            ),
            contentPadding: const EdgeInsets.symmetric(
              vertical: 12,
              horizontal: 12,
            ),
            filled: true,
            fillColor: Colors.grey.shade50,
          ),
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
          maxLength: 7,
          maxLengthEnforcement: MaxLengthEnforcement.enforced,
          style: const TextStyle(fontSize: 14),
        ),
      ],
    ),
  );
  }
}

class _ConnectionInfo extends StatelessWidget {
  final bool isConnected;
  final String brokerHost;
  final int brokerPort;
  final String topicSensors;
  final String topicPidParams;
  final String topicSetpoint;

  const _ConnectionInfo({
  required this.isConnected,
  required this.brokerHost,
  required this.brokerPort,
  required this.topicSensors,
  required this.topicPidParams,
  required this.topicSetpoint,
  });

  @override
  Widget build(BuildContext context) {
  return Card(
    elevation: 2,
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    color: isConnected ? Colors.green.shade50 : Colors.red.shade50,
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                isConnected ? Icons.check_circle : Icles.error,
                color: isConnected ? Colors.green : Colors.red,
                size: 20,
              ),
              const SizedBox(width: 8),
              Text(
                isConnected ? 'Connected to MQTT Broker' : 'Disconnected',
                style: TextStyle(
                  color: isConnected ? Colors.green : Colors.red,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            'Broker: $brokerHost:$brokerPort',
            style: const TextStyle(fontSize: 12, color: Colors.grey),
          ),
          const SizedBox(height: 4),
          Text(
            'Sensors Topic: $topicSensors',
            style: const TextStyle(fontSize: 12, color: Colors.grey),
          ),
          const SizedBox(height: 4),
          Text(
            'PID Topic: $topicPidParams',
            style: const TextStyle(fontSize: 12, color: Colors.grey),
          ),
          const SizedBox(height: 4),
          Text(
            'Setpoint Topic: $topicSetpoint',
            style: const TextStyle(fontSize: 12, color: Colors.grey),
          ),
        ],
      ),
    ),
  );
  }
}