import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    TextPart,
    UserPromptPart,
)

from core.agent import create_research_agent
from core.models import check_if_model_is_available, get_list_of_models


def convert_to_pydantic_messages(
    messages: list[dict[str, str]],
) -> list[ModelMessage]:
    """Convert Streamlit chat messages to Pydantic AI message format."""
    result: list[ModelMessage] = []
    for msg in messages:
        if msg["role"] == "user":
            result.append(ModelRequest(parts=[UserPromptPart(content=msg["content"])]))
        else:
            result.append(ModelResponse(parts=[TextPart(content=msg["content"])]))
    return result


def reset_conversation() -> None:
    """Clear the conversation history."""
    st.session_state.messages = []


EMBEDDING_MODEL = "nomic-embed-text"
DEFAULT_MODEL = "qwen3:14b"
DEFAULT_FOLDER = "Research"

if "list_of_models" not in st.session_state:
    st.session_state["list_of_models"] = get_list_of_models()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar layout
with st.sidebar:
    # New Chat button at top
    st.button(
        "New Chat",
        on_click=reset_conversation,
        type="primary",
        use_container_width=True,
    )
    st.divider()

    # Settings section - pre-select default model if available
    model_list = st.session_state["list_of_models"]
    default_index = model_list.index(DEFAULT_MODEL) if DEFAULT_MODEL in model_list else 0
    selected_model = st.selectbox("Model:", model_list, index=default_index)
    folder_path = st.text_input("Documents folder:", DEFAULT_FOLDER)

# Validate folder path
valid_folder = folder_path and os.path.isdir(folder_path)
if folder_path and not valid_folder:
    st.error(
        "The provided path is not a valid directory. Please enter a valid folder path."
    )

# Initialize or reinitialize agent when model or folder changes
if valid_folder and (
    "agent" not in st.session_state
    or st.session_state.get("ollama_model") != selected_model
    or st.session_state.get("folder_path") != folder_path
):
    # Only reload vector store if folder changed (not when model changes)
    folder_changed = st.session_state.get("folder_path") != folder_path
    first_load = "agent" not in st.session_state

    # Clean up old agent to prevent stale LanceDB references
    if "agent" in st.session_state:
        del st.session_state["agent"]

    st.session_state["ollama_model"] = selected_model
    st.session_state["folder_path"] = folder_path

    need_reload = folder_changed or first_load

    # Ensure models are available (will auto-pull if missing)
    with st.spinner("Checking model availability..."):
        try:
            check_if_model_is_available(selected_model)
            check_if_model_is_available(EMBEDDING_MODEL)
        except Exception as e:
            st.error(f"Error with Ollama models: {e}")
            st.stop()

    spinner_msg = "Loading documents..." if need_reload else "Switching model..."
    with st.spinner(spinner_msg):
        try:
            st.session_state.agent = create_research_agent(
                llm_model=selected_model,
                embedding_model=EMBEDDING_MODEL,
                documents_path=folder_path,
                reload=need_reload,
            )
        except Exception as e:
            st.error(f"Error initializing agent: {e}")
            st.stop()

# Re-index button in sidebar
with st.sidebar:
    if valid_folder and st.button("Re-index Documents"):
        # Clean up old agent to prevent stale LanceDB references
        if "agent" in st.session_state:
            del st.session_state["agent"]

        try:
            with st.spinner("Re-indexing documents..."):
                st.session_state.agent = create_research_agent(
                    llm_model=selected_model,
                    embedding_model=EMBEDDING_MODEL,
                    documents_path=folder_path,
                    reload=True,
                )
            st.success("Documents re-indexed!")
        except Exception as e:
            st.error(f"Error re-indexing: {e}")

    # Document status indicator
    st.divider()
    if "agent" in st.session_state and valid_folder:
        doc_count = len(st.session_state.agent.vector_store)
        st.info(f"Loaded {doc_count} document chunks")
    elif not folder_path:
        st.warning("Enter a folder path")
    elif not valid_folder:
        st.warning("Invalid folder path")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.empty()  # Prevent ghost text on rerun (Streamlit #9239)

# Welcome message when no conversation
if not st.session_state.messages and "agent" in st.session_state:
    st.markdown(
        """
### Welcome!

I can answer questions about your documents using RAG (Retrieval-Augmented Generation).
"""
    )

# Chat interface
if "agent" in st.session_state:
    if prompt := st.chat_input("Question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"), st.container():
            try:
                # Convert previous messages to Pydantic format for context
                # Exclude the current user message (last one) as it's passed separately
                history = convert_to_pydantic_messages(st.session_state.messages[:-1])

                # Get streaming handler with tool call info
                stream = st.session_state.agent.get_streaming_chat_handler(
                    include_tool_calls=True
                )(prompt, message_history=history)

                response_placeholder = st.empty()
                response_text = ""
                searches_made: list[str] = []

                # Animated status with search logging
                with st.status("Thinking...", expanded=True) as status:
                    for event_type, content in stream:
                        if event_type == "tool_call":
                            query = content["args"].get("query", "documents")
                            searches_made.append(query)
                            status.update(label=f"Searching: {query}")
                            st.write(f"🔍 {query}")
                        elif event_type == "text":
                            if not response_text:  # First text chunk
                                if searches_made:
                                    n = len(searches_made)
                                    word = "query" if n == 1 else "queries"
                                    label = f"Searched {n} {word}"
                                else:
                                    label = "Responding..."
                                status.update(label=label, expanded=False)
                            response_text += content
                            response_placeholder.markdown(response_text)
                    # Final status
                    if searches_made:
                        n = len(searches_made)
                        word = "query" if n == 1 else "queries"
                        status.update(label=f"Searched {n} {word}", state="complete")
                    else:
                        status.update(label="Complete", state="complete")

                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
            except Exception as e:
                st.error(f"Error processing question: {e}")
else:
    st.warning("Initializing agent...")
    st.chat_input("Question", disabled=True)
