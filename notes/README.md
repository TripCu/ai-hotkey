# Notes Directory

Place Markdown (`.md`, `.markdown`, `.mdx`) files here to expose them to the AI runtime.  
Files remain local; nothing is uploaded. The backend scores each note for keyword overlap with the current
prompt and injects the most relevant snippets into the LLM context.

Tips:
- Keep private notes out of source control (see `.gitignore`).
- Organize subfolders however you like; the search is recursive.
- Large notes are truncated to ~1,200 characters per response.

You can also point `.env:NOTES_PATH` at another folder (absolute or relative).
