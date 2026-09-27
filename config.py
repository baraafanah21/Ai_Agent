# Maximum characters read from a single file before truncating.
MAX_CHARS = 10000

# Seconds a child Python process may run before it is killed.
TIMEOUT_SECONDS = 30

# Directory the agent is allowed to touch. Never supplied by the model.
WORKING_DIR = "./calculator"

# Model used for every request. The free router (openrouter/free) picks a
# different model per call, which makes tool selection unreliable, so pin one.
MODEL = "cohere/north-mini-code:free"

# Upper bound on agent loop turns, to stop runaway token burn.
MAX_ITERATIONS = 20

# Largest tool result sent back to the model, to keep prompt tokens bounded.
MAX_TOOL_RESULT_CHARS = 10000
