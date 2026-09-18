AI Coding Agent

A lightweight coding agent built from scratch in Python to explore the core concepts behind modern AI coding assistants.

The project uses an OpenAI-compatible API and gives the model access to a small set of controlled tools for inspecting, modifying, and executing code.

Features

* List files and directories
* Read file contents
* Create and modify files
* Execute Python files
* Support positional arguments when running files
* Handle multiple tool calls through an agent loop
* Verify changes by running code after modifications

Architecture

A traditional chatbot follows:

User → LLM → Response

This project extends that workflow:

User
 ↓
LLM
 ↓
Tool Call
 ↓
Python Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Final Response

The agent can repeat this process until the task is completed.

Agent Loop

The core workflow is:

Inspect → Read → Understand → Modify → Test → Verify → Answer

The messages list maintains the conversation state, including assistant messages, tool calls, and tool results.

Tools

The agent provides four tools:

* get_files_info — inspect files and directories
* get_file_content — read files
* write_file — create or modify files
* run_python_file — execute Python files

Filesystem operations are restricted to a designated working directory, with path validation to prevent directory traversal.

Technologies

* Python
* OpenAI Python SDK
* OpenRouter
* JSON
* subprocess
* Function calling

Example

The agent can receive a task such as:

Fix the bug in the calculator.

It can then inspect the relevant files, identify the problem, modify the code, run the program, and verify the result before responding.

Purpose

This project was built as a practical exercise in understanding:

* AI agents
* Function calling
* Tool integration
* Agent loops
* Conversation state
* Filesystem interaction
* Basic tool security

The implementation is intentionally small and educational, focusing on understanding the underlying architecture rather than building a production-ready coding assistant.