#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <stack>
#include <set>
using namespace std;

struct Directory {
    string name;
    unordered_map<string, Directory*> children;
    Directory* parent;

    // Constructor to initialize the Directory object
    Directory(string n, Directory* p) : name(n), parent(p) {}
};

void deleteDirectory(Directory* dir) {
    for (auto& child : dir->children) {
        deleteDirectory(child.second);
    }
    delete dir;
}

int main(int argc, char* argv[]) {
    int num_files = 0, total_depth = 0, max_depth = 0;
    int curr_depth = 0;

    // Correct initialization of root directory
    Directory* root = new Directory("root", nullptr);
    Directory* curr_dir = root;
    vector<string> curr_dir_string{"/"};
    set<string> curr_dir_ls;
    vector<string> max_dir_string;
    string filename = argv[1];
    ifstream file(filename);
    string line;
    string lastLine;
    getline(file, line); // Skip the first line as it's always "cd /" - told by judge
    
    while (!lastLine.empty() || getline(file, line)) {
        if (!lastLine.empty()) {
            line = lastLine;
            lastLine.clear();
        }

        stringstream ss(line);
        string command, arg;
        ss >> command >> arg;

        if (arg == "ls") {
            string curr_path;
            if (curr_dir_ls.find(curr_path) != curr_dir_ls.end()) {
                continue;
            }
            for (const auto& s : curr_dir_string) {
                curr_path += s;
            }
            while (getline(file, line) && line[0] != '$') {
                ss.clear();
                ss.str(line);
                string type, name;
                ss >> type >> name;
                if (type == "dir") {
                    curr_dir->children[name] = new Directory(name, curr_dir);
                    curr_depth++;
                    if (curr_depth > max_depth) {
                        max_depth = curr_depth;
                        max_dir_string = curr_dir_string;
                        max_dir_string.push_back(name + "/");
                    }
                    curr_depth--;
                } else {
                    if (curr_depth == max_depth) {
                        max_dir_string = curr_dir_string;
                        max_dir_string.push_back(name);
                    }
                    total_depth += curr_depth;
                    num_files++;
                }
            }
            curr_dir_ls.insert(curr_path);
            lastLine = line; // Store the last line that caused the loop to exit
        } else if (arg == "cd") {
            string path;
            ss >> path;
            if (path == "/") {
                curr_depth = 0;
                curr_dir_string = {"/"};
                curr_dir = root;
            } else if (path == ".." && curr_depth != 0) {
                curr_depth--;
                curr_dir = curr_dir->parent;
                curr_dir_string.pop_back();
            } else {
                curr_depth++;
                curr_dir_string.push_back(path + "/");
                if (curr_dir->children.find(path) == curr_dir->children.end()) {
                    curr_dir->children[path] = new Directory(path, curr_dir);
                }
                curr_dir = curr_dir->children[path];
                if (curr_depth > max_depth) {
                    max_depth = curr_depth;
                    max_dir_string = curr_dir_string;
                }
            }
        }
    }

    double average = num_files == 0 ? 0 : std::round(static_cast<double>(total_depth) / num_files * 10) / 10;
    cout << "Number of files: " << num_files << ", Average depth: " << average << ", Deepest directory: ";
    for (const auto& dir : max_dir_string) {
        cout << dir;
    }
    cout << endl;

    deleteDirectory(root);
    return 0;
}
