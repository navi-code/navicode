import os
import json

from navicode.parsers.python.parse_comments import comment_parser

def navicode_init():
    cur_dir = os.getcwd()

    python_files = []

    for dirpath, _, files in os.walk(cur_dir):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            if fname.endswith('.py'):
                python_files.append(fname)

    if len(python_files) > 0:
        dirname = os.path.basename(cur_dir)

        comments_dump = {}
        for i, python_file in enumerate(python_files):
            print(f"[{i+1}/{len(python_files)}] Scanning {python_file}")
            comments = comment_parser(python_file)
            filename = python_file[python_file.index(dirname):]
            for comment in comments:
                if filename in comments_dump.keys():
                    comments_dump[filename].append(comment)
                else:
                    comments_dump[filename] = [comment]

        with open(dirname + '_navi.json', 'w') as file:
            json.dump(comments_dump, file, indent=4)