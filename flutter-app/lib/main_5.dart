import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
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
            ],
          )
        ),
      ),
    ),
  );
}
