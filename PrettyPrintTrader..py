from Npp import *

INDENT_TRADER = ""
INDENT_CATEGORY = " " * 4
INDENT_ITEM = " " * 8
COLUMN_SPACING = " " * 4
TAB_WIDTH = 4


def format_category_items(items):
    if not items:
        return []

    # Sort alphabetically by item name
    items.sort(key=lambda x: x['name'].lower())

    # Find longest item name in this category
    max_len = max(len(item['name']) for item in items)

    formatted = []
    for item in items:
        padding = " " * (max_len - len(item['name']))
        line = (
            INDENT_ITEM +
            item['name'] + "," +
            padding + COLUMN_SPACING +
            item['v1'] + "," + COLUMN_SPACING +
            item['v2'] + "," + COLUMN_SPACING +
            item['v3']
        )
        if item['comment']:
            line += " // " + item['comment']
        formatted.append(line)

    return formatted


def pretty_print_trader():
    lines = editor.getText().splitlines()
    output = []

    current_items = []

    first_trader = True
    first_category = True

    for raw_line in lines:
        line = raw_line.replace("\t", " " * TAB_WIDTH)
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Skip full-line comments
        if stripped.startswith("//"):
            continue

        # Trader
        if stripped.startswith("<Trader>"):
            if current_items:
                output.extend(format_category_items(current_items))
                current_items = []

            if not first_trader:
                output.append("")

            first_trader = False
            first_category = True

            output.append(INDENT_TRADER + stripped)
            continue

        # Category
        if stripped.startswith("<Category>"):
            if current_items:
                output.extend(format_category_items(current_items))
                current_items = []

            if not first_category:
                output.append("")

            first_category = False
            output.append(INDENT_CATEGORY + stripped)
            continue

        # Ignore other <Something>
        if stripped.startswith("<") and stripped.endswith(">"):
            continue

        # Item line
        if "," in stripped:
            comment = ""
            code = line
            if "//" in line:
                code, comment = line.split("//", 1)
                comment = comment.strip()

            parts = [p.strip() for p in code.split(",")]
            if len(parts) >= 4:
                current_items.append({
                    "name": parts[0],
                    "v1": parts[1],
                    "v2": parts[2],
                    "v3": parts[3],
                    "comment": comment
                })
            continue

    # Flush last category
    if current_items:
        output.extend(format_category_items(current_items))

    editor.beginUndoAction()
    editor.setText("\n".join(output))
    editor.endUndoAction()

    console.show()
    console.clear()
    console.write("Pretty print completed (Python 2 compatible).\n")


pretty_print_trader()
