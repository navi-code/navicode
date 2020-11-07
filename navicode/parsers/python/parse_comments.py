import tokenize

def comment_parser(py_source_file):
    comments = []

    line_num = 1

    with open(py_source_file, "r") as file:
        tokens = tokenize.generate_tokens(file.readline)
        for token in tokens:
            if token.type == 55:
                comments.append((token.string.strip(), line_num))
            elif token.type == 3 and token.string.startswith('"""'):
                comments.append((token.string.strip(), line_num))
            elif token.type == 4 or token.type == 56:
                line_num += 1

    return comments