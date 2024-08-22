#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <sstream>
#include <limits>
#include <cmath>
#include <tuple>
#include <chrono>
#include <fstream> 

#define FASTIO                \
    ios ::sync_with_stdio(0); \
    cin.tie(0);               \
    cout.tie(0);

#define pb push_back
#define mt make_tuple
using namespace std;


int manhatten(int i, int j, int m, int n) {
    return abs(m - 1 - i) + abs(n - 1 - j);
}
int euclidean(int x, int y, int m, int n) {
    return sqrt(pow(m - x - 1, 2) + pow(n - y - 1, 2));
}

// find the shortest path in a matrix from a given file path
int shortestPath(const string& filePath) {
    ifstream file(filePath);
    if (!file.is_open()) {
        cerr << "Unable to open file" << endl;
        return -1;
    }

    // Parse the input file into a 1D vector of integers for improved spatial locality
    vector<int> matrix;
    string line;
    int n = 0; // Width of the matrix
    while (getline(file, line)) { //memmap
        int size = 0;
        for (char c : line) {
            if (!isdigit(c)) continue;
            matrix.pb(c - '0');
            size++;
        }
        if (n == 0) {
            n = size;
        }
    }

    file.close();

    int m = matrix.size() / n; // Height of the matrix
    if (m == 0 || n == 0) {
        return 0;
    }

    // Initialize the distance map as a 1D vector for improved spatial locality
    vector<int> dist(m * n, numeric_limits<int>::max());
    dist[0] = 0;

    using Node = tuple<int, int, int>; // (f, w, index)
    priority_queue<Node, vector<Node>, greater<Node>> pq;
    pq.push(mt(manhatten(0, 0, m, n), 0, 0));

    while (!pq.empty()) {
        auto [f, w, index] = pq.top();
        pq.pop();
        int i = index / n, j = index % n;

        if (i == m - 1 && j == n - 1) {
            return w + matrix[index];
        }

        for (auto [di, dj] : vector<pair<int, int>>{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}) {
            int ni = i + di, nj = j + dj;
            if (0 <= ni && ni < m && 0 <= nj && nj < n) {
                int newIndex = ni * n + nj;
                int new_w = w + matrix[index];
                if (new_w < dist[newIndex]) {
                    dist[newIndex] = new_w;
                    pq.push(mt(new_w + manhatten(ni, nj, m, n), new_w, newIndex));
                }
            }
        }
    }

    return dist[m * n - 1] + matrix[m * n - 1];
}

int main(int argc, char* argv[]) {
    FASTIO;
    if (argc != 2) {
        cout << "Usage: " << argv[0] << " <file_path>" << endl;
        return 1;
    }
    string filePath = argv[1];
    cout << shortestPath(filePath) << endl;
    return 0;
}
