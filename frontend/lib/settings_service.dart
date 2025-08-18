import 'package:shared_preferences/shared_preferences.dart';

class SettingsService {
  static const _backendUrlKey = 'backend_url';
  static const _defaultBackendUrl = 'http://127.0.0.1:8000';

  Future<String> getBackendUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_backendUrlKey) ?? _defaultBackendUrl;
  }

  Future<void> setBackendUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_backendUrlKey, url);
  }
}
