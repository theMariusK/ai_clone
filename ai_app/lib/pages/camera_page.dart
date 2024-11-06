import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:ai_app/pages/video_page.dart';

class CameraPage extends StatefulWidget {
  const CameraPage({Key? key}) : super(key: key);

  @override
  _CameraPageState createState() => _CameraPageState();
}

class _CameraPageState extends State<CameraPage> {
  bool _isLoading = true;
  bool _isRecording = false;
  late CameraController _cameraController;
  List<CameraDescription> _cameras = [];
  int _selectedCameraIndex = 0; // 0 for back, 1 for front

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  @override
  void dispose() {
    _cameraController.dispose();
    super.dispose();
  }

  Future<void> _initCamera() async {
    _cameras = await availableCameras();
    _setCamera(_selectedCameraIndex);
  }

  Future<void> _setCamera(int index) async {
    final selectedCamera = _cameras[index];
    _cameraController = CameraController(selectedCamera, ResolutionPreset.max);
    await _cameraController.initialize();
    setState(() => _isLoading = false);
  }

  void _toggleCamera() async {
    setState(() => _isLoading = true);
    _selectedCameraIndex = (_selectedCameraIndex + 1) % _cameras.length;
    await _cameraController.dispose();
    await _setCamera(_selectedCameraIndex);
  }

  Future<void> _recordVideo() async {
    if (_isRecording) {
      final file = await _cameraController.stopVideoRecording();
      setState(() => _isRecording = false);
      final route = MaterialPageRoute(
        fullscreenDialog: true,
        builder: (_) => VideoPage(filePath: file.path),
      );
      Navigator.push(context, route);
    } else {
      await _cameraController.prepareForVideoRecording();
      await _cameraController.startVideoRecording();
      setState(() => _isRecording = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Container(
        color: Colors.white,
        child: const Center(
          child: CircularProgressIndicator(),
        ),
      );
    } else {
      return Center(
        child: Stack(
          alignment: Alignment.bottomCenter,
          children: [
            CameraPreview(_cameraController),
            Positioned(
              top: 50,
              right: 20,
              child: FloatingActionButton(
                onPressed: _toggleCamera,
                child: const Icon(Icons.flip_camera_android),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(25),
              child: FloatingActionButton(
                backgroundColor: Colors.red,
                child: Icon(_isRecording ? Icons.stop : Icons.circle),
                onPressed: _recordVideo,
              ),
            ),
          ],
        ),
      );
    }
  }
}
