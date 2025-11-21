#include <boost/asio.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

using boost::asio::ip::tcp;

std::vector<char> read_image_file(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary | std::ios::ate);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filename);
    }

    std::streamsize size = file.tellg();
    file.seekg(0, std::ios::beg);

    std::vector<char> buffer(size);
    if (!file.read(buffer.data(), size)) {
        throw std::runtime_error("Error reading file");
    }

    return buffer;
}

std::string get_content_type(const std::string& path) {
    if (path.ends_with(".jpg") || path.ends_with(".jpeg")) return "image/jpeg";
    if (path.ends_with(".png")) return "image/png";
    if (path.ends_with(".gif")) return "image/gif";
    if (path.ends_with(".bmp")) return "image/bmp";
    return "application/octet-stream";
}

std::string make_http_response(const std::vector<char>& image_data, const std::string& content_type) {
    std::ostringstream response;
    response << "HTTP/1.1 200 OK\r\n";
    response << "Content-Type: " << content_type << "\r\n";
    response << "Content-Length: " << image_data.size() << "\r\n";
    response << "Connection: close\r\n";
    response << "\r\n";

    std::string header = response.str();
    std::string full_response = header + std::string(image_data.begin(), image_data.end());

    return full_response;
}

void handle_client(tcp::socket& socket, const std::string& image_path) {
    try {
        char buffer[1024];
        boost::system::error_code error;

        size_t length = socket.read_some(boost::asio::buffer(buffer), error);
        if (error == boost::asio::error::eof) {
            return;
        }
        else if (error) {
            throw boost::system::system_error(error);
        }

        std::cout << "Request from client:\n" << std::string(buffer, length) << "\n";

        std::vector<char> image_data = read_image_file(image_path);
        std::string content_type = get_content_type(image_path);

        std::string response = make_http_response(image_data, content_type);

        boost::asio::write(socket, boost::asio::buffer(response), error);

        std::cout << "Sent image, size: " << image_data.size() << " bytes\n";

    }
    catch (std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
}

int main() {
    try {
        std::string image_path = "D:/test-data/thumbnail.png";

        std::cout << "Checking file: " << image_path << "\n";
        std::ifstream test(image_path);
        if (!test.good()) {
            std::cerr << "ERROR: File " << image_path << " not found!\n";
            std::cerr << "Place an image file next to the .exe file\n";
            return 1;
        }
        test.close();

        boost::asio::io_context io_context;
        tcp::acceptor acceptor(io_context, tcp::endpoint(tcp::v4(), 8080));

        std::cout << "HTTP server started on port 8080\n";
        std::cout << "Open browser: http://127.0.0.1:8080\n";
        std::cout << "Or run the client to receive the image\n\n";

        while (true) {
            tcp::socket socket(io_context);
            acceptor.accept(socket);
            std::cout << "\n=== New connection ===\n";
            handle_client(socket, image_path);
        }

    }
    catch (std::exception& e) {
        std::cerr << "Critical error: " << e.what() << "\n";
    }

    return 0;
}