# """Chat interface for the main agent."""


# async def chat_stream(agent, user_message: str, thread_id: str = 'main-session'):
#     """Stream chat response token by token with status updates.

#     Args:
#         agent: The main agent instance
#         user_message: User's input message
#         thread_id: Conversation thread identifier

#     Yields:
#         Dictionaries with event type and content:
#         - {"type": "token", "content": "text chunk"}
#         - {"type": "status", "content": "Tool execution status"}
#         - {"type": "done", "content": "full response"}
#     """
#     config = {'configurable': {'thread_id': thread_id}}
#     input_data = {'messages': [{'role': 'user', 'content': user_message}]}

#     full_response = ""
#     tools_completed = False  # Flag to start streaming only after tools finish

#     try:
#         async for event in agent.astream_events(input_data, config, version="v2"):
#             event_type = event.get("event", "")

#             # Tool execution started
#             if event_type == "on_tool_start":
#                 tool_name = event.get("name", "tool")
#                 yield {"type": "status", "content": f"🔄 Running {tool_name}..."}

#             # Tool execution completed
#             elif event_type == "on_tool_end":
#                 tool_name = event.get("name", "tool")
#                 tools_completed = True  # Now we can start streaming clean responses
#                 yield {"type": "status", "content": f"✅ Completed {tool_name}"}

#             # Stream LLM tokens (only AFTER tools complete)
#             elif event_type == "on_chat_model_stream" and tools_completed:
#                 chunk = event.get("data", {}).get("chunk")
#                 if chunk and hasattr(chunk, "content") and chunk.content:
#                     content = chunk.content

#                     # Skip if this looks like a ToolMessage representation (starts with "content=")
#                     if content.strip().startswith("content="):
#                         continue

#                     full_response += content
#                     yield {"type": "token", "content": content}

#         # Clean the full_response if it contains tool metadata
#         clean_response = full_response
#         if "tool_call_id=" in full_response:
#             # Extract only the text after the last closing quote of tool_call_id='xxx'
#             import re
#             # Find the last occurrence of tool_call_id='...' and take text after it
#             matches = list(re.finditer(r"tool_call_id='[^']*'", full_response))
#             if matches:
#                 last_match = matches[-1]
#                 clean_response = full_response[last_match.end():].strip()

#         # Send completion marker with cleaned response
#         yield {"type": "done", "content": clean_response}

#     except Exception as e:
#         yield {"type": "error", "content": f"Error: {str(e)}"}


# async def chat(agent, user_message: str, thread_id: str = 'main-session') -> str:
#     """Send a message to the agent and get response.

#     Args:
#         agent: The main agent instance
#         user_message: User's input message
#         thread_id: Conversation thread identifier

#     Returns:
#         Agent's response text
#     """
#     config = {'configurable': {'thread_id': thread_id}}
#     response = await agent.ainvoke(
#         {'messages': [{'role': 'user', 'content': user_message}]},
#         config=config,
#     )
#     ai_message = response['messages'][-1]
#     return ai_message.content if hasattr(ai_message, 'content') else str(ai_message)


# async def run_chat(agent):
#     """Run interactive chat loop.

#     Args:
#         agent: The main agent instance
#     """
#     thread_id = 'session-1'
#     print('SAP Assistant ready. Type "exit" to quit.\n')
#     while True:
#         user_input = input('You: ').strip()
#         if not user_input:
#             continue
#         if user_input.lower() in ('exit', 'quit'):
#             break
#         response = await chat(agent, user_input, thread_id=thread_id)
#         print(f'\nAssistant: {response}\n')

"""Chat interface for the main agent."""


async def chat(agent, user_message: str, config: dict = None) -> str:
    """Send a message to the agent and get response.

    Args:
        agent: The main agent instance
        user_message: User's input message
        config: Configuration dict with thread_id and session_id

    Returns:
        Agent's response text
    """
    if not config:
        config = {'configurable': {'thread_id': 'main-session'}}

    response = await agent.ainvoke(
        {'messages': [{'role': 'user', 'content': user_message}]},
        config=config,
    )
    ai_message = response['messages'][-1]
    return ai_message.content if hasattr(ai_message, 'content') else str(ai_message)


async def run_chat(agent):
    """Run interactive chat loop.

    Args:
        agent: The main agent instance
    """
    thread_id = 'session-1'
    config = {
        'configurable': {
            'thread_id': thread_id,
            'session_id': thread_id  # Use same as thread_id for CLI
        }
    }
    print('SAP Assistant ready. Type "exit" to quit.\n')
    while True:
        user_input = input('You: ').strip()
        if not user_input:
            continue
        if user_input.lower() in ('exit', 'quit'):
            break
        response = await chat(agent, user_input, config=config)
        print(f'\nAssistant: {response}\n')