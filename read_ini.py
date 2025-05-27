def read_simple_ini(filename):
    """
    Read a simple config file with lines like `key = value`
    Ignores blank lines and lines starting with '#'.
    Returns a dict of key -> value (strings).
    """
    config = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                config[key.strip()] = val.strip()
    return config

def write_simple_ini(filename, config, header_lines=None):
    """
    Write the config dict back to file.
    If header_lines provided, write them first (list of strings).
    """
    with open(filename, 'w') as f:
        if header_lines:
            for hl in header_lines:
                f.write(hl.rstrip() + '\n')
        for key, val in config.items():
            f.write(f"{key} = {val}\n")

def get_header_lines(filename):
    """
    Return lines that are comments or blank lines before first key=value.
    Useful to preserve header comments.
    """
    header_lines = []
    with open(filename, 'r') as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                header_lines.append(line.rstrip('\n'))
            else:
                # Found first key=value line
                break
    return header_lines

def replace_ini_values(filepath, replacements):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        if not stripped or stripped.startswith('#') or '=' not in line:
            new_lines.append(line)
            continue

        key, sep, rest = line.partition('=')
        key_strip = key.strip()
        if key_strip in replacements:
            indent = line[:line.find(key_strip)]
            new_value = replacements[key_strip]
            # Remove trailing newline if present
            new_value = new_value.strip('\n')
            new_line = f"{indent}{key_strip} = {new_value}\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(filepath, 'w') as f:
        f.writelines(new_lines)
