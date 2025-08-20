import 'package:flutter/material.dart';
import 'decision_service.dart';

class MbtiResultPage extends StatefulWidget {
  final List<String> answers;

  const MbtiResultPage({super.key, required this.answers});

  @override
  State<MbtiResultPage> createState() => _MbtiResultPageState();
}

class _MbtiResultPageState extends State<MbtiResultPage> {
  final DecisionService _decisionService = DecisionService();
  Future<MbtiAnalysisResponse>? _analysisResult;

  @override
  void initState() {
    super.initState();
    _analysisResult = _decisionService.getMbtiResult(MbtiAnalysisRequest(answers: widget.answers));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('你的 MBTI 分析結果'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: FutureBuilder<MbtiAnalysisResponse>(
          future: _analysisResult,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const CircularProgressIndicator();
            } else if (snapshot.hasError) {
              return Text('分析失敗: ${snapshot.error}');
            } else if (snapshot.hasData) {
              final result = snapshot.data!;
              return Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      result.mbtiType,
                      style: Theme.of(context).textTheme.displayMedium?.copyWith(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      result.summary,
                      style: Theme.of(context).textTheme.headlineSmall,
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 24),
                    Text(
                      result.description,
                      style: Theme.of(context).textTheme.bodyLarge,
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 48),
                    ElevatedButton(
                      onPressed: () {
                        Navigator.of(context).pop();
                      },
                      child: const Text('返回主頁'),
                    )
                  ],
                ),
              );
            } else {
              return const Text('沒有收到分析結果。');
            }
          },
        ),
      ),
    );
  }
}
