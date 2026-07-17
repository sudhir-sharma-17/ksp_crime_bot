with open("backend/app/agent.py", "r") as f:
    content = f.read()

# 1. Patch context string building
old_context_build = """        else:
            truncated = results[:5]
            res_str = str(truncated)
            if len(res_str) > 1000:
                res_str = res_str[:1000] + "... [truncated]"
            context_str += f"Data (up to 5 rows):\\n{res_str}\\n\""""

new_context_build = """        else:
            total_rows = len(results)
            if results and isinstance(results[0], dict) and 'Total_Matching_Records' in results[0]:
                total_rows = results[0]['Total_Matching_Records']
            truncated = results[:5]
            res_str = str(truncated)
            if len(res_str) > 1000:
                res_str = res_str[:1000] + "... [truncated]"
            context_str += f"The database returned {total_rows} total records. Here is a sample of the top 5 records for context:\\n{res_str}\\n\""""

content = content.replace(old_context_build, new_context_build)

# 2. Patch System Prompt with DATA SUMMARY RULE
old_sys_prompt_start = """    system_prompt = (
        "You are an elite State Intelligence AI for the KSP. You must structure all your responses using advanced Markdown.\\n\""""

new_sys_prompt_start = """    system_prompt = (
        "You are an elite State Intelligence AI for the KSP. You must structure all your responses using advanced Markdown.\\n"
        "DATA SUMMARY RULE: When summarizing SQL results, you will be given the TOTAL row count and a small data sample. You MUST state the true total row count in your analysis (e.g., 'The database found 800 records'). You MUST NEVER claim the total data size is only 5 rows just because you were only shown a 5-row sample. Base your summary on the total count provided.\\n\\n\""""

content = content.replace(old_sys_prompt_start, new_sys_prompt_start)

with open("backend/app/agent.py", "w") as f:
    f.write(content)

print("Agent patched for total count injection and summary rule.")
