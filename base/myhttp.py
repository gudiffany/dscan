import socket


def parse_http_request(request):
    headers, body = request.split('\n', 1)
    method, path, protocol = headers.split(' ')
    headers_dict = {}
    body = body.split('\n')
    tmp_dict = ''
    for header in body:
        try:
            key, value = header.split(': ', 1)
            headers_dict[key] = value
            # print(headers_dict)
        except:
            if header != '':
                tmp_dict += header
    tmp_dict = tmp_dict.split('&')
    body_dict = {}
    if tmp_dict:
        for tmp in tmp_dict:
            try:
                key, value = tmp.split('=', 1)
                body_dict[key] = value
            except:
                break
    return {
        'Method': method,
        'Path': path,
        'Protocol': protocol,
        'Headers': headers_dict,
        'Body': body_dict
    }


def http_to_requests(request, host):
    request_dict = parse_http_request(request)
    res = '''import requests\n'''
    res += f'Headers = {request_dict["Headers"]}\n'
    res += f'data = {request_dict["Body"]}\n'
    if request_dict['Method'] == "GET":
        res += f'r = requests.get(\'{host + request_dict["Path"]}\',headers=Headers)\n'
    elif request_dict['Method'] == "POST":
        res += f'r = requests.post(\'{host + request_dict["Path"]}\',headers=Headers,data=data)\n'
    res += 'print(r.text)'
    print(res)


def insert_into_http_request(original_request, string_to_insert):
    request_parts = original_request.split('\n\n', 1)
    updated_request = request_parts[0] + '\n' + string_to_insert + '\n\n'
    if len(request_parts) > 1:
        updated_request += request_parts[1]
    return updated_request


def http_to_socket(request, host):
    if "Connection: close" not in request:
        request = insert_into_http_request(request, "Connection: close")
    if "Host: " not in request:
        request = insert_into_http_request(request, f"Host: {host}")
    formatted_request = request.replace('\n', '\r\n')
    formatted_request += '\r\n'
    return formatted_request


def send_raw_http_request(host, port, request):
    request = http_to_socket(request, host)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.sendall(request.encode())
        response = b''
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data
        return response.decode()
    finally:
        s.close()
