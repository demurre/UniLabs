#include <boost/asio.hpp>
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>

using boost::asio::ip::tcp;

struct HttpResponse {
    int status_code;
    std::string headers;
    std::vector<char> body;
};

HttpResponse parse_http_response(const std::vector<char>& data) {
    HttpResponse response;

    std::string data_str(data.begin(), data.end());
    size_t header_end = data_str.find("\r\n\r\n");

    if (header_end == std::string::npos) {
        throw std::runtime_error("Invalid HTTP response format");
    }

    response.headers = data_str.substr(0, header_end);

    size_t status_pos = response.headers.find(' ');
    if (status_pos != std::string::npos) {
        std::string status_str = response.headers.substr(status_pos + 1, 3);
        response.status_code = std::stoi(status_str);
    }

    size_t body_start = header_end + 4; 
    response.body.assign(data.begin() + body_start, data.end());

    return response;
}

void save_image(const std::vector<char>& image_data, const std::string& filename) {
    std::ofstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot create file: " + filename);
    }

    file.write(image_data.data(), image_data.size());
    file.close();

    std::cout << "Image saved to file: " << filename << "\n";
    std::cout << "File size: " << image_data.size() << " bytes\n";
}

void send_http_request(tcp::socket& socket, const std::string& host, const std::string& path) {
    std::string request =
        "GET " + path + " HTTP/1.1\r\n" +
        "Host: " + host + "\r\n" +
        "Connection: close\r\n\r\n";

    std::cout << "Sending request:\n" << request << "\n";

    boost::asio::write(socket, boost::asio::buffer(request));

    std::vector<char> response_data;
    char buffer[4096];
    boost::system::error_code error;

    while (true) {
        size_t length = socket.read_some(boost::asio::buffer(buffer), error);

        if (length > 0) {
            response_data.insert(response_data.end(), buffer, buffer + length);
        }

        if (error == boost::asio::error::eof) {
            break; 
        }
        else if (error) {
            throw boost::system::system_error(error);
        }
    }

    std::cout << "Received " << response_data.size() << " bytes of data\n\n";

    HttpResponse response = parse_http_response(response_data);

    std::cout << "=== HTTP Headers ===\n";
    std::cout << response.headers << "\n\n";

    if (response.status_code == 200) {
        std::cout << "Status: 200 OK - Success!\n";
        save_image(response.body, "received_image.jpg");
    }
    else {
        std::cout << "Status: " << response.status_code << " - Error!\n";
    }
}

int main() {
    try {
        boost::asio::io_context io_context;

        tcp::resolver resolver(io_context);
        tcp::resolver::results_type endpoints = resolver.resolve("127.0.0.1", "8080");

        tcp::socket socket(io_context);
        std::cout << "Connecting to server 127.0.0.1:8080...\n";
        boost::asio::connect(socket, endpoints);
        std::cout << "Connection established!\n\n";

        send_http_request(socket, "127.0.0.1", "/");

        std::cout << "\n=== Done! ===\n";
        std::cout << "Check file 'received_image.jpg' in the program folder\n";

    }
    catch (std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        std::cerr << "\nMake sure the server is running!\n";
    }

    return 0;
}