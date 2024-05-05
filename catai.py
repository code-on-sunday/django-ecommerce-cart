import os
import argparse
import fnmatch


def is_binary(file_path):
    """Check if a file is binary, excluding certain file extensions."""
    # List of extensions to exclude from being considered as binary
    excluded_extensions = [".svg", ".json"]

    # Check the file extension
    if any(file_path.endswith(ext) for ext in excluded_extensions):
        return True  # Not considered binary if it has an excluded extension

    try:
        with open(file_path, "rb") as file:
            for _ in range(512):  # Read the first 512 bytes
                if b"\0" in file.read(512):
                    return True
        return False
    except IOError:
        return True


def read_catignore(directory):
    """Read the .catignore file and return a list of patterns."""
    catignore_path = os.path.join(directory, ".gitignore")
    if os.path.exists(catignore_path):
        with open(catignore_path, "r") as file:
            patterns = [line.strip() for line in file if line.strip()]
        return patterns
    return []


def should_ignore(file_path, ignore_patterns):
    """Check if a file or folder should be ignored based on ignore patterns."""
    relative_path = os.path.relpath(file_path)
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(relative_path, pattern):
            return True
        if pattern.endswith("/") and relative_path.startswith(pattern):
            return True
    return False


def concatenate_files(files, ignore_patterns):
    """Concatenate content of files and print to stdout."""
    for file_path in files:
        if not is_binary(file_path) and not should_ignore(file_path, ignore_patterns):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    print(
                        f"# >>>>> Starting contents of file {file_path} >>>>>\n{file.read()}\n# <<<<< End of contents of file {file_path} <<<<<"
                    )
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        else:
            print(f">>>>> Skipping file: {file_path} <<<<<")


def main():
    parser = argparse.ArgumentParser(
        description="Concatenate files in specified folders or specified files."
    )
    parser.add_argument("paths", nargs="+", help="Paths to files or folders")
    args = parser.parse_args()

    ignore_patterns = []
    files = []

    root_folder = os.path.abspath(os.path.dirname(__file__))
    ignore_patterns.extend(read_catignore(root_folder))

    for path in args.paths:
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            ignore_patterns.extend(read_catignore(path))
            for root, _, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    files.append(file_path)

    concatenate_files(files, ignore_patterns)


if __name__ == "__main__":
    main()
