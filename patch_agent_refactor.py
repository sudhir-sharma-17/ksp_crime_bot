import re

with open("backend/app/agent.py", "r") as f:
    content = f.read()

old_chart = """        "CHART METADATA GENERATION:\\n"
        "At the very end of your response, you MUST include a strict JSON block wrapped in ```json ... ``` that defines a chart for the data if applicable.\\n"
        "Format:\\n"
        "```json\\n"
        "{\\n"
        "  \\"type\\": \\"pie\\" or \\"bar\\" or \\"none\\",\\n"
        "  \\"data\\": [ {\\"name\\": \\"Category1\\", \\"value\\": 10}, {\\"name\\": \\"Category2\\", \\"value\\": 20} ]\\n"
        "}\\n"
        "```\\n"
        "Only generate 'pie' or 'bar' if the data is aggregated (like counts, totals). Otherwise, return type 'none'."
    )"""

new_chart = """        "CHART METADATA GENERATION:\\n"
        "At the very end of your response, you MUST include a strict JSON block wrapped in ```json ... ``` that defines a chart for the data if applicable.\\n"
        "If the user asks for a 'breakdown', 'distribution', 'comparison', 'count', or explicitly requests a chart, you MUST set `type` to 'pie' or 'bar'.\\n"
        "Identify the text column for `label_column` and the numerical count/sum column for `value_column`.\\n"
        "Format:\\n"
        "```json\\n"
        "{\\n"
        "  \\"type\\": \\"pie\\" or \\"bar\\" or \\"none\\",\\n"
        "  \\"label_column\\": \\"column_name_for_labels\\",\\n"
        "  \\"value_column\\": \\"column_name_for_values\\"\\n"
        "}\\n"
        "```\\n"
        "Only generate 'pie' or 'bar' if the data is aggregated (like counts, totals). Otherwise, return type 'none'."
    )"""

content = content.replace(old_chart, new_chart)

old_extract = """    # Extract JSON chart metadata
    chart_metadata = {"type": "none", "data": []}"""
new_extract = """    # Extract JSON chart metadata
    chart_metadata = {"type": "none", "label_column": "", "value_column": ""}"""

content = content.replace(old_extract, new_extract)

with open("backend/app/agent.py", "w") as f:
    f.write(content)
print("Agent prompt refactored")
