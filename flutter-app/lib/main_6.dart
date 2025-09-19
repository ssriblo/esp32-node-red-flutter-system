import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      theme: ThemeData(fontFamily: 'IndieFlower'),
      home: Scaffold(
        backgroundColor: Colors.grey,
        appBar: AppBar(
          backgroundColor: Colors.blue,
          title: Text('Adding Assets'),
          centerTitle: true,
        ),
        body: Center(
          child: Stack(
            children: <Widget>[
              Image(image: AssetImage('assets/images/bg.jpg')
              ),
              Image.asset('assets/icons/icon.png'),
              Positioned(
                top: 350,
                left: 40,
                child: Text(
                  'My custom font',
                  style: TextStyle(
                    // fontFamily: 'CustomFont',
                    fontSize: 38,
                    color: Colors.red,
                    // fontFamily: 'IndieFlower',
                  ),
                )
              )
            ],
          )
        ),
      ),
    ),
  );
}
