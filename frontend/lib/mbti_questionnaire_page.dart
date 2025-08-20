import 'package:flutter/material.dart';
import 'decision_service.dart';
import 'mbti_result_page.dart';

class MbtiQuestionnairePage extends StatefulWidget {
  const MbtiQuestionnairePage({super.key});

  @override
  State<MbtiQuestionnairePage> createState() => _MbtiQuestionnairePageState();
}

class _MbtiQuestionnairePageState extends State<MbtiQuestionnairePage> {
  final DecisionService _decisionService = DecisionService();
  String _question = "載入中...";
  List<String> _possibleAnswers = [];
  bool _isOutcome = false;
  String? _currentNodeId;
  final String _treeId = "mbti_questionnaire";
  final List<String> _userAnswers = [];

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
        _possibleAnswers = response.possibleAnswers ?? [];
      });

      if (_isOutcome) {
        _navigateToResult();
      }
    } catch (e) {
      setState(() {
        _question = "無法載入問卷，請確認後端伺服器是否正在運行。";
        _possibleAnswers = [];
        _isOutcome = true;
      });
    }
  }

  void _handleAnswer(String answer) {
    // Extract the MBTI letter from the answer string, e.g., "E: ..." -> "E"
    final mbtiLetter = answer.split(":")[0];
    _userAnswers.add(mbtiLetter);

    if (_currentNodeId != null) {
      final request = DecisionRequest(
        treeId: _treeId,
        currentNodeId: _currentNodeId,
        answer: answer,
      );
      _fetchDecision(request);
    }
  }

  void _navigateToResult() {
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (context) => MbtiResultPage(answers: _userAnswers),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MBTI 性格分析問卷'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
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
                ..._possibleAnswers.map((answer) {
                  // Display only the text part of the answer
                  final answerText = answer.substring(answer.indexOf(":") + 2);
                  return Container(
                    width: double.infinity,
                    margin: const EdgeInsets.only(bottom: 12.0),
                    child: ElevatedButton(
                      onPressed: () => _handleAnswer(answer),
                      child: Text(answerText),
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
