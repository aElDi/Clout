import 'dart:io';
import 'dart:ffi';

var scanners = [];

void pluginsScan() async {
  List<String> mm = [];
  var path = Directory('.\\modules');
  try {
    await for (var module in path.list(followLinks: false)) {
      mm.add(module.path);
    }
  } catch (e) {
    print(e);
  }
  for (var lib in mm
      .where((filename) => filename.substring(8).split(".")[1] == "aot")) {
        
        final DynamicLibrary md5Library = DynamicLibrary.open(lib);
      }
  ;
}
