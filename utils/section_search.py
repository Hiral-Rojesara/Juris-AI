import re

def search_section(text, section_no):

    pattern = rf"^{section_no}\."

    lines = text.split("\n")

    result = []

    capture = False

    for line in lines:

        line = line.strip()

        if re.match(pattern, line):
            capture = True

        elif capture and re.match(r"^\d+\.", line):
            break

        if capture:
            result.append(line)

    return "\n".join(result)