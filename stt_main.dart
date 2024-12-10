import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:http/http.dart' as http;
import 'package:flutter_tts/flutter_tts.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Speech to Text & TTS Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: SpeechToTextPage(),
    );
  }
}

class SpeechToTextPage extends StatefulWidget {
  @override
  _SpeechToTextPageState createState() => _SpeechToTextPageState();
}

class _SpeechToTextPageState extends State<SpeechToTextPage> {
  late stt.SpeechToText _speech;
  final FlutterTts _flutterTts = FlutterTts();
  
  bool _isListening = false;
  String _recognizedText = "";
  String _responseText = "";

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _initializeSpeech();
  }

  Future<void> _initializeSpeech() async {
    bool available = await _speech.initialize(
      onStatus: (status) {
        // Monitor recognition status
        if (status == 'done') {
          setState(() {
            _isListening = false;
          });
          _sendToServer(_recognizedText);
        }
      },
      onError: (error) {
        print("Speech error: $error");
      },
    );

    if (!mounted) return;
    setState(() {
      _isListening = false;
    });
  }

  void _startListening() async {
    setState(() {
      _recognizedText = "";
      _responseText = "";
    });
    await _speech.listen(
      onResult: (result) {
        setState(() {
          _recognizedText = result.recognizedWords;
        });
      },
    );
    setState(() {
      _isListening = true;
    });
  }

  void _stopListening() async {
    await _speech.stop();
    setState(() {
      _isListening = false;
    });
    _sendToServer(_recognizedText);
  }

  Future<void> _sendToServer(String text) async {
    String url = "http://192.168.88.4:5000/input";

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"text": text}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        String responseText = data["response"] ?? "No response field";
        setState(() {
          _responseText = responseText;
        });
        _speak(responseText); // Speak out the server's response
      } else {
        setState(() {
          _responseText = "Server returned status ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        _responseText = "Error connecting to server: $e";
      });
    }
  }

  Future<void> _speak(String text) async {
    await _flutterTts.setLanguage("en-US");
    await _flutterTts.setPitch(1.0);
    await _flutterTts.speak(text);
  }

  @override
  Widget build(BuildContext context) {
    bool canListen = _speech.isAvailable;

    return Scaffold(
      appBar: AppBar(
        title: Text('Speech to Text & TTS Demo'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            Text(
              "Tap the microphone and start speaking. After processing, the app will respond and speak the server's reply.",
              style: TextStyle(fontSize: 16.0),
            ),
            SizedBox(height: 20),
            ElevatedButton.icon(
              icon: Icon(_isListening ? Icons.mic_off : Icons.mic),
              label: Text(_isListening ? "Stop Listening" : "Start Listening"),
              onPressed: canListen
                  ? () {
                      if (_isListening) {
                        _stopListening();
                      } else {
                        _startListening();
                      }
                    }
                  : null,
            ),
            SizedBox(height: 20),
            Text("Recognized Text:", style: TextStyle(fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            Text(_recognizedText),
            SizedBox(height: 20),
            Text("Server Response:", style: TextStyle(fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            Text(_responseText),
          ],
        ),
      ),
    );
  }
}
