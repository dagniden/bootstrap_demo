# dont add into git

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def __get_index(self):
        with open('templates/contacts.html', 'r', encoding='utf-8') as f:
            return f.read()

    def do_GET(self):
        page_content = self.__get_index()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Декодируем данные
        post_data_decoded = post_data.decode('utf-8')

        # Парсим данные формы
        post_params = parse_qs(post_data_decoded)

        # Выводим в консоль все полученные данные
        print("\n" + "="*50)
        print("Получен POST-запрос")
        print("="*50)
        print("Сырые данные:", post_data_decoded)
        print("\nРазобранные данные:")
        for key, value in post_params.items():
            print(f"  {key}: {value[0]}")
        print("="*50 + "\n")

        # Отправляем ответ пользователю
        response = """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Спасибо</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-success" role="alert">
                    <h4 class="alert-heading">Спасибо!</h4>
                    <p>Ваше сообщение успешно получено.</p>
                    <hr>
                    <a href="/" class="btn btn-primary">Вернуться на главную</a>
                </div>
            </div>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(response, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
