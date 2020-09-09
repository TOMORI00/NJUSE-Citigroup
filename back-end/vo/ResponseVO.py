from flask import Flask, jsonify, request, make_response


def build_success(content):
    data = {'success': True, 'message': None, 'content': content}
    return jsonify(data)


def build_failure(message):
    data = {'success': False, 'message': message, 'content': None}
    return jsonify(data)
