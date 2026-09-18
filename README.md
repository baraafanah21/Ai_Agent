AI Coding Agent

A lightweight AI coding agent built from scratch in Python using an OpenAI-compatible API.

This project was built as a hands-on exploration of how AI coding agents work internally, including LLM interaction, function calling, tool execution, agent loops, filesystem operations, and code execution.

The goal was not to build a production-ready coding assistant, but to understand the core architecture behind tools such as Claude Code, Cursor Agent, and other agentic coding systems.

⸻

🚀 Features

The agent can:

* Inspect files and directories
* Read file contents
* Create or overwrite files
* Execute Python files
* Pass command-line arguments to Python programs
* Automatically decide which tools to use
* Execute multiple tool calls in sequence
* Inspect results and continue working
* Verify changes by running the relevant code

⸻

🧠 How It Works

A normal chatbot follows a simple flow:

User
  ↓
LLM
  ↓
Answer

An AI agent adds the ability to interact with the environment:

User
  ↓
LLM
  ↓
Tool Call
  ↓
Python executes the tool
  ↓
Tool Result
  ↓
LLM
  ↓
Another Tool Call / Final Answer

The agent can therefore follow a loop of:

THINK → ACT → OBSERVE → THINK → ACT → ...

The LLM decides what it wants to do, while the Python application controls what it is actually allowed to do.

⸻

🛠️ Available Tools

get_files_info

Lists files and directories inside the allowed working directory.

Example:

- main.py: file_size=1234 bytes, is_dir=False
- pkg: file_size=4096 bytes, is_dir=True

get_file_content

Reads the contents of a file.

The tool also limits the number of characters that can be read to prevent extremely large files from consuming excessive context.

write_file

Creates or overwrites a file with the provided content.

The tool also creates missing parent directories when necessary.

run_python_file

Executes a Python file with optional command-line arguments.

It captures:

* stdout
* stderr
* exit code

and applies a timeout to prevent an execution from running indefinitely.

⸻

🔐 Path Security

The agent’s filesystem tools are restricted to a specific working directory.

Before accessing a path, the tools normalize and validate it using functions such as:

os.path.abspath()
os.path.normpath()
os.path.commonpath()

This prevents requests such as:

../secret.txt

from escaping the permitted workspace.

The working_directory is also injected by the Python application instead of being exposed to the LLM as a tool argument.

This creates an important security boundary:

LLM
 ↓
Tool Request
 ↓
Python Validation
 ↓
Filesystem

The model cannot directly access the filesystem.

⸻

🔄 Agent Loop

The core of the project is the agent loop.

Conceptually:

for _ in range(20):
    response = client.chat.completions.create(...)
    message = response.choices[0].message
    messages.append(message)
    if not message.tool_calls:
        print(message.content)
        break
    for tool_call in message.tool_calls:
        result = call_function(tool_call)
        messages.append(result)

The loop allows the model to perform multiple actions before producing its final response.

For example, fixing a bug might look like:

User: Fix the calculator bug
        ↓
Inspect files
        ↓
Read calculator.py
        ↓
Understand the bug
        ↓
Write the fix
        ↓
Run the program/tests
        ↓
Verify the result
        ↓
Final response

⸻

🔧 Function Calling

The model does not directly execute Python functions.

Instead, it produces a structured tool call containing:

* Function name
* Arguments
* Tool call ID

The application then maps the requested function to an actual Python function.

Conceptually:

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

The arguments returned by the model are JSON, so they are converted into Python data using:

json.loads(...)

Then the selected function is executed.

⸻

🧩 Tool Results

After a tool executes, its result is sent back to the LLM as a message with:

role: tool
tool_call_id: ...
content: ...

The tool_call_id connects the result to the original tool call.

This allows the model to understand:

"I asked the system to read calculator.py,
and this is what came back."

⸻

💾 Conversation State

The messages list acts as the agent’s working memory.

It contains the conversation history, including:

User messages
Assistant responses
Tool calls
Tool results

This is essential because the model needs previous tool results to decide what to do next.

For example:

Assistant → Read calculator.py
Tool → [file contents]
Assistant → I found the bug
Assistant → Write calculator.py
Tool → Successfully wrote file
Assistant → Run calculator
Tool → Output: 17
Assistant → Fixed and verified

Without the message history, the model would lose this context.

⸻

🧠 System Prompt

The agent is instructed to follow a workflow similar to:

Inspect
  ↓
Read
  ↓
Understand
  ↓
Modify
  ↓
Test
  ↓
Verify
  ↓
Answer

This helps prevent the model from claiming that something was fixed without actually verifying it.

⸻

📁 Project Structure

.
├── main.py
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/
│   ├── main.py
│   ├── pkg/
│   │   ├── calculator.py
│   │   └── render.py
│   └── tests.py
├── .env
└── README.md

The exact structure may vary depending on the stage of the project.

⸻

⚙️ Technologies

* Python
* OpenAI Python SDK
* OpenRouter
* JSON
* argparse
* subprocess
* File-system APIs
* Function calling
* Tool-based agent architecture

⸻

▶️ Running the Agent

Install the required dependencies and configure the API key:

OPENROUTER_API_KEY=your_api_key

Then run:

uv run main.py "Fix the bug in the calculator"

Verbose mode:

uv run main.py "Fix the bug in the calculator" --verbose

⸻

🧪 Example

Suppose the calculator contains a precedence bug:

3 + 7 * 2

The correct result is:

17

The agent can inspect the project, identify the incorrect precedence configuration, modify the file, and execute the calculator to verify the result.

Expected final output:

17

⸻

🔑 Key Concepts Learned

This project was built to understand the fundamentals behind agentic systems.

LLM vs Agent

An LLM primarily generates responses.

An agent combines an LLM with:

LLM
+
Tools
+
Environment
+
Execution Loop
+
State

Function Calling

The model can request actions using structured tool calls instead of directly executing code.

Tool Integration

Python functions become capabilities that the model can request.

Agent Loop

The model can repeatedly:

Think → Act → Observe

until the task is complete.

Security Boundaries

The model should not be trusted with unrestricted filesystem or command execution.

The application must validate and control what tools are allowed to do.

⸻

⚠️ Security Considerations

This project is intentionally educational and should not be treated as a production-safe coding agent.

Giving an AI agent access to:

* Files
* File writing
* Code execution
* Shell commands

can introduce serious security risks.

A production implementation would require stronger isolation, permissions, sandboxing, resource limits, authentication, auditing, and additional validation.

⸻

🎯 Future Improvements

Possible extensions include:

* Add more tools
* Add test-running tools
* Support more programming languages
* Add Git integration
* Add shell command execution with stronger sandboxing
* Improve error handling
* Add streaming responses
* Add tool permission controls
* Add persistent memory
* Support multiple LLM providers
* Add automated test generation
* Build a terminal-based UI
* Run tools inside isolated containers

⸻

📚 What This Project Demonstrates

This project provides a small but practical implementation of the core architecture behind modern agentic coding assistants.

The main takeaway is:

             ┌─────────────┐
             │     User    │
             └──────┬──────┘
                    ↓
             ┌─────────────┐
             │     LLM     │
             └──────┬──────┘
                    ↓
              Tool Request
                    ↓
             ┌─────────────┐
             │    Python   │
             │    Tools    │
             └──────┬──────┘
                    ↓
               Tool Result
                    ↓
             ┌─────────────┐
             │     LLM     │
             └──────┬──────┘
                    ↓
             Final Response

Building this system from scratch makes the underlying mechanics of AI agents, function calling, tool use, and agent loops much easier to understand.
