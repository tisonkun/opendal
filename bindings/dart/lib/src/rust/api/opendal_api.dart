// This file is automatically generated, so please do not edit it.
// @generated by `flutter_rust_bridge`@ 2.8.0.

// ignore_for_file: invalid_use_of_internal_member, unused_import, unnecessary_import

import '../frb_generated.dart';
import 'package:flutter_rust_bridge/flutter_rust_bridge_for_generated.dart';

// Rust type: RustOpaqueMoi<flutter_rust_bridge::for_generated::RustAutoOpaqueInner<Metadata>>
abstract class Metadata implements RustOpaqueInterface {
  /// Content-Disposition of this object
  String? get contentDisposition;

  /// Content Length of this object
  BigInt? get contentLength;

  /// Content MD5 of this object.
  String? get contentMd5;

  /// Content Type of this object.
  String? get contentType;

  /// ETag of this object.
  String? get etag;

  /// Returns true if the <op.stat> object describes a file system directory.
  bool get isDirectory;

  /// Returns true if the <op.stat> object describes a regular file.
  bool get isFile;

  /// Last Modified of this object.
  ///
  /// We will output this time in RFC3339 format like `1996-12-19T16:39:57+08:00`.
  String? get lastModified;
}

// Rust type: RustOpaqueMoi<flutter_rust_bridge::for_generated::RustAutoOpaqueInner<Operator>>
abstract class Operator implements RustOpaqueInterface {
  Future<void> check();

  Future<void> createDir({required String path});

  void createDirSync({required String path});

  Future<void> delete({required String path});

  void deleteSync({required String path});

  Future<bool> isExist({required String path});

  bool isExistSync({required String path});

  factory Operator(
          {required String schemeStr, required Map<String, String> map}) =>
      RustLib.instance.api
          .crateApiOpendalApiOperatorNew(schemeStr: schemeStr, map: map);

  Future<void> rename({required String from, required String to});

  void renameSync({required String from, required String to});

  Future<Metadata> stat({required String path});

  Metadata statSync({required String path});
}
