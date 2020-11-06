def parser(py_source_file):
    comments = {"single_line": [], "docstring": []}

    with open(py_source_file, "r") as file:
        tokens = tokenize.generate_tokens(file.readline)
        for token in tokens:
            if token.type == 55:
                comments['single_line'].append(token.string)
            elif token.type == 3 and token.string.startswith('"""'):
                comments['docstring'].append(token.string)

    return comments