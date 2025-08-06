import re

def parse_markdown_testcases(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.findall(r'#### Testcase #\d+\n```(.*?)```', content, re.DOTALL)

    testcases = []
    for block in blocks:
        block = block.strip()
        match = re.search(r":\s+", block)
        if not match:
            continue

        split_index = match.end()
        prompt = block[:split_index]
        remaining = block[split_index:]

        if '\n' in remaining:
            input_line, output_text = remaining.split('\n', 1)
            output_text = output_text.strip()
        else:
            input_line = remaining.strip()
            output_text = ""

        # Reconstruct expected stdout
        full_expected = f"{prompt}{output_text}\n"
        testcases.append((input_line + "\n", full_expected))

    return testcases

