import argparse
class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.children = {} # only directory is stored
        self.parent = parent

def main(filename):
    num_files, total_depth, max_depth = 0, 0, 0
    curr_depth = 0
    root = curr_dir = Directory("root", None)
    curr_dir_string = ["/"]
    curr_dir_ls = set()
    max_dir_string = []
    with open(filename, 'r') as file:
        content = file.read().splitlines()
    # Told by a judge that the first line is always cd /
    line_count = 1
    while line_count < len(content):
        line_split = content[line_count].split()
        if line_split[1] == "ls":
            line_count += 1
            if ''.join(curr_dir_string) in curr_dir_ls:
                while content[line_count][0] != '$':
                    line_count += 1
                continue
            line = content[line_count].split()
            while line_count < len(content) and line[0] != '$':
                if line[0] == "dir":
                    curr_dir.children[line[1]] = Directory(line[1], curr_dir)
                    if curr_depth + 1 > max_depth:
                        max_depth = curr_depth + 1
                        max_dir_string = curr_dir_string.copy()
                        max_dir_string.append(line[1] + "/")
                else:
                    if curr_depth == max_depth:
                        max_dir_string = curr_dir_string.copy()
                        max_dir_string.append(line[1])
                    total_depth += curr_depth
                    num_files += 1
                line_count += 1
                if line_count < len(content):
                    line = content[line_count].split()
            curr_dir_ls.add(''.join(curr_dir_string))
            
        elif line_split[1] == "cd":
            if line_split[2] == "/":
                curr_depth = 0
                curr_dir_string = ["/"]
                curr_dir = root
            elif line_split[2] == ".." and curr_depth != 0:
                curr_depth -= 1
                curr_dir = curr_dir.parent
                curr_dir_string.pop()
            else:
                curr_depth += 1
                curr_dir_string.append(line_split[2] + "/")
                if curr_dir.children.get(line_split[2]) is None:
                    curr_dir.children[line_split[2]] = Directory(line_split[2], curr_dir)
                curr_dir = curr_dir.children[line_split[2]]
                if curr_depth > max_depth:
                    max_depth = curr_depth
                    max_dir_string = curr_dir_string.copy()
                
            line_count += 1
    average = 0 if num_files == 0 else total_depth / num_files
    return (num_files, average, ''.join(max_dir_string))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='The file to process')
    args = parser.parse_args()
    print(main(args.filename))
