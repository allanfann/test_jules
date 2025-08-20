import 'dart:convert';
import 'package:http/http.dart' as http;
import 'settings_service.dart';

class DecisionRequest {
  final String treeId;
  final String? currentNodeId;
  final String? answer;

  DecisionRequest({required this.treeId, this.currentNodeId, this.answer});

  Map<String, dynamic> toJson() {
    return {
      'tree_id': treeId,
      'current_node_id': currentNodeId,
      'answer': answer,
    };
  }
}

class DecisionResponse {
  final String treeId;
  final String nodeId;
  final String nodeType;
  final String text;
  final List<String>? possibleAnswers;

  DecisionResponse({
    required this.treeId,
    required this.nodeId,
    required this.nodeType,
    required this.text,
    this.possibleAnswers,
  });

  factory DecisionResponse.fromJson(Map<String, dynamic> json) {
    return DecisionResponse(
      treeId: json['data']['tree_id'],
      nodeId: json['data']['node_id'],
      nodeType: json['data']['node_type'],
      text: json['data']['text'],
      possibleAnswers: json['data']['possible_answers'] != null
          ? List<String>.from(json['data']['possible_answers'])
          : null,
    );
  }
}

class MbtiAnalysisRequest {
  final List<String> answers;

  MbtiAnalysisRequest({required this.answers});

  Map<String, dynamic> toJson() {
    return {
      'answers': answers,
    };
  }
}

class MbtiAnalysisResponse {
  final String mbtiType;
  final String summary;
  final String description;

  MbtiAnalysisResponse({
    required this.mbtiType,
    required this.summary,
    required this.description,
  });

  factory MbtiAnalysisResponse.fromJson(Map<String, dynamic> json) {
    return MbtiAnalysisResponse(
      mbtiType: json['mbti_type'],
      summary: json['summary'],
      description: json['description'],
    );
  }
}

class DecisionService {
  final SettingsService _settingsService = SettingsService();

  Future<DecisionResponse> decide(DecisionRequest request) async {
    final backendUrl = await _settingsService.getBackendUrl();
    final response = await http.post(
      Uri.parse('$backendUrl/api/v1/decide'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(request.toJson()),
    );

    if (response.statusCode == 200) {
      return DecisionResponse.fromJson(jsonDecode(utf8.decode(response.bodyBytes)));
    } else {
      throw Exception('Failed to load decision from backend');
    }
  }

  Future<MbtiAnalysisResponse> getMbtiResult(MbtiAnalysisRequest request) async {
    final backendUrl = await _settingsService.getBackendUrl();
    final response = await http.post(
      Uri.parse('$backendUrl/api/v1/mbti_analysis'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(request.toJson()),
    );

    if (response.statusCode == 200) {
      return MbtiAnalysisResponse.fromJson(jsonDecode(utf8.decode(response.bodyBytes)));
    } else {
      throw Exception('Failed to load MBTI result from backend');
    }
  }
}
