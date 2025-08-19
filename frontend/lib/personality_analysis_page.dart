
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PersonalityAnalysisScreen extends StatefulWidget {
  const PersonalityAnalysisScreen({super.key});

  @override
  State<PersonalityAnalysisScreen> createState() =>
      _PersonalityAnalysisScreenState();
}

class _PersonalityAnalysisScreenState extends State<PersonalityAnalysisScreen> {
  final TextEditingController _textController = TextEditingController();
  String? _personality;
  Map<String, dynamic>? _scores;
  bool _isLoading = false;
  String? _error;

  Future<void> _analyzeText() async {
    if (_textController.text.isEmpty) {
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final response = await http.post(
        Uri.parse('http://localhost:8000/api/v1/legacy/personality_analysis'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'text': _textController.text}),
      );

      if (response.statusCode == 200) {
        final result = jsonDecode(utf8.decode(response.bodyBytes));
        setState(() {
          _personality = result['personality'];
          _scores = Map<String, dynamic>.from(result['scores']);
        });
      } else {
        setState(() {
          _error = 'Failed to get analysis. Status code: ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Failed to connect to the server. Make sure it is running.';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Personality Analysis'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              TextField(
                controller: _textController,
                decoration: const InputDecoration(
                  labelText: 'Enter text for analysis',
                  border: OutlineInputBorder(),
                ),
                maxLines: 5,
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _isLoading ? null : _analyzeText,
                child: _isLoading
                    ? const CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      )
                    : const Text('Analyze'),
              ),
              const SizedBox(height: 24),
              if (_error != null)
                Text(
                  _error!,
                  style: const TextStyle(color: Colors.red, fontSize: 16),
                  textAlign: TextAlign.center,
                ),
              if (_personality != null) ...[
                Text(
                  'Personality: $_personality',
                  style: Theme.of(context).textTheme.headlineSmall,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 16),
                if (_scores != null) ...[
                  const Text(
                    'Scores:',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        children: _scores!.entries.map((entry) {
                          return Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(entry.key, style: const TextStyle(fontSize: 16)),
                              Text(entry.value.toString(),
                                  style: const TextStyle(fontSize: 16)),
                            ],
                          );
                        }).toList(),
                      ),
                    ),
                  ),
                ]
              ],
            ],
          ),
        ),
      ),
    );
  }
}
