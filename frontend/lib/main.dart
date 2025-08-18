import 'package:flutter/material.dart';
import 'decision_service.dart';
import 'settings_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Decision Tree App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const DecisionScreen(),
    );
  }
}

class DecisionScreen extends StatefulWidget {
  const DecisionScreen({super.key});

  @override
  State<DecisionScreen> createState() => _DecisionScreenState();
}

class _DecisionScreenState extends State<DecisionScreen> {
  final DecisionService _decisionService = DecisionService();
  String _question = "Loading...";
  List<String> _answers = [];
  bool _isOutcome = false;
  String? _currentNodeId;
  final String _treeId = "sample_tree"; // You might want to make this dynamic

  @override
  void initState() {
    super.initState();
    _fetchDecision(DecisionRequest(treeId: _treeId));
  }

  Future<void> _fetchDecision(DecisionRequest request) async {
    try {
      final response = await _decisionService.decide(request);
      setState(() {
        _question = response.text;
        _currentNodeId = response.nodeId;
        _isOutcome = response.nodeType == 'OUTCOME';
        _answers = response.possibleAnswers ?? [];
      });
    } catch (e) {
      setState(() {
        _question =
            "Failed to load decision. Make sure the backend is running.";
        _answers = [];
        _isOutcome = true;
      });
    }
  }

  void _handleAnswer(String answer) {
    if (_currentNodeId != null) {
      final request = DecisionRequest(
        treeId: _treeId,
        currentNodeId: _currentNodeId,
        answer: answer,
      );
      _fetchDecision(request);
    }
  }

  void _navigateToSettings() {
    Navigator.of(context)
        .push(
      MaterialPageRoute(builder: (context) => const SettingsPage()),
    )
        .then((_) {
      // Refetch the decision tree when returning from settings
      _fetchDecision(DecisionRequest(treeId: _treeId));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Decision Tree'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: _navigateToSettings,
          ),
        ],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text(
                _question,
                style: Theme.of(context).textTheme.headlineMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              if (!_isOutcome)
                ..._answers.map((answer) {
                  return Container(
                    width: double.infinity,
                    margin: const EdgeInsets.only(bottom: 12.0),
                    child: ElevatedButton(
                      onPressed: () => _handleAnswer(answer),
                      child: Text(answer),
                    ),
                  );
                }),
            ],
          ),
        ),
      ),
    );
  }
}
