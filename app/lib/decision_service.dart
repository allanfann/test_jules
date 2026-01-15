import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

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

class DecisionService {
  static const String _urlKey = 'backend_url';
  static const String _defaultUrl = 'http://127.0.0.1:8000';

  Future<String> _getBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_urlKey) ?? _defaultUrl;
  }

  Future<DecisionResponse> decide(DecisionRequest request) async {
    final baseUrl = await _getBaseUrl();
    final fullUrl = '$baseUrl/api/v1/decide';

    final response = await http.post(
      Uri.parse(fullUrl),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(request.toJson()),
    );

    if (response.statusCode == 200) {
      // The backend seems to send a response with UTF-8 encoding,
      // so we need to decode it properly.
      return DecisionResponse.fromJson(jsonDecode(utf8.decode(response.bodyBytes)));
    } else {
      throw Exception('Failed to load decision from backend. Status code: ${response.statusCode}');
    }
  }
}
