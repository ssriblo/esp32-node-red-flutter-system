import 'package:flutter/material.dart';
import 'dart:async';

// void main() => runApp(MyFirstApp(height: 100));
void main() => runApp(MyFirstApp());

class MyFirstApp extends StatefulWidget { 
  @override
  State<StatefulWidget> createState() {
    return _MyFirstAppState();
  }

}
  // const MyFirstApp({super.key, required int height});
class _MyFirstAppState extends State<MyFirstApp> {
  late bool _loading;
  late double _progressValue;

  @override
  void initState() {
    super.initState();
    _loading = false;
    _progressValue = 0.0;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        backgroundColor: Colors.green,
        appBar: AppBar(title: Text('My First App'), centerTitle: true),
        body: Center(
          child: Container(
            padding: EdgeInsets.all(16),
            child: _loading ? 
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                LinearProgressIndicator(value: _progressValue),
                Text(
                  '${(_progressValue * 100).round()}%',
                  style: TextStyle(color: Colors.white, fontSize: 20),
                ),
              ],
            )
            : Text(
                  'Press the button to download',
                  style: TextStyle(color: Colors.white, fontSize: 20),
                ),
          ),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: (){
            setState(() {
              _loading = !_loading;
              _updateProgress();
            });
          },
          backgroundColor: Colors.blue,
          child: Icon(Icons.cloud_download, color: Colors.white),
        ),
      ),
    );
  }


  void _updateProgress() {
    const oneSec = const Duration(seconds: 1);
    Timer.periodic(oneSec, (Timer t) {
      setState(() {
        _progressValue += 0.2;
        if (_progressValue >= 1.0) {
          _loading = false;
          _progressValue = 0.0;
          t.cancel();
          return;
        }
      });
    });
  } 
}