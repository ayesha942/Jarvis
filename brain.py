# # ============================================================
# #  BRAIN MODULE
# #  Connects to Claude AI (Anthropic API) to answer questions
# #  This is the "intelligence" of Jarvis
# # ============================================================

# import anthropic
# import config

# class Brain:
#     """
#     The Brain uses the Anthropic Claude API to answer any question
#     that isn't handled by a specific command module.
    
#     CONCEPT: Large Language Models (LLMs)
#     Claude is an LLM — a neural network trained on massive amounts of text.
#     It predicts the most likely next token (word piece) given your input.
#     The result feels like "understanding" because it has learned patterns
#     from billions of documents about how conversations, facts, and 
#     reasoning work.
    
#     CONCEPT: API (Application Programming Interface)
#     An API is a way for your code to talk to someone else's service.
#     We send: your question (as JSON over HTTPS)
#     We receive: Claude's answer (as JSON)
#     We pay: per token (input tokens + output tokens)
    
#     CONCEPT: Tokens
#     Text is split into tokens (roughly 3/4 of a word).
#     "Hello world" = 2 tokens
#     "Artificial intelligence" = 3 tokens
#     Pricing and context limits are measured in tokens.
#     """

#     def __init__(self):
#         # Create Anthropic client — handles authentication and HTTP
#         # It automatically reads ANTHROPIC_API_KEY from environment
#         # or you can pass it explicitly as shown below
#         self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
#         # Conversation history — enables multi-turn conversations
#         # Each item: {"role": "user"/"assistant", "content": "text"}
#         self.conversation_history = []
        
#         print("🧠 AI Brain initialized")

#     def ask(self, question: str) -> str:
#         """
#         Send a question to Claude and get a response.
        
#         CONCEPT: Messages API
#         Claude uses a "messages" format (like chat):
#         - "user" messages = what you say
#         - "assistant" messages = what Claude says
#         - "system" message = instructions that always apply
        
#         CONCEPT: Context Window
#         Claude remembers the full conversation_history each API call.
#         This is why it can remember what you said 3 messages ago.
#         But there's a limit (200k tokens for Claude) — very old messages
#         eventually need to be dropped (we handle this below).
#         """
#         # Add the new question to history
#         self.conversation_history.append({
#             "role": "user",
#             "content": question
#         })
        
#         # Keep history manageable — last 20 messages only
#         # This prevents hitting context limits and saves API costs
#         if len(self.conversation_history) > 20:
#             self.conversation_history = self.conversation_history[-20:]
        
#         try:
#             # Make the API call
#             response = self.client.messages.create(
#                 model=config.AI_MODEL,
#                 max_tokens=config.AI_MAX_TOKENS,
                
#                 # System prompt = Jarvis's personality & instructions
#                 # This is NOT part of conversation_history — it's separate
#                 system=config.AI_SYSTEM_PROMPT,
                
#                 # Send full conversation so Claude has context
#                 messages=self.conversation_history
#             )
            
#             # Extract the text from the response
#             # response.content is a list of ContentBlock objects
#             # We want the text from the first (usually only) block
#             answer = response.content[0].text
            
#             # Add Claude's response to history for next turn
#             self.conversation_history.append({
#                 "role": "assistant",
#                 "content": answer
#             })
            
#             return answer
            
#         except anthropic.AuthenticationError:
#             return "My API key seems invalid. Please check the config file."
#         except anthropic.RateLimitError:
#             return "I'm being rate limited. Please wait a moment."
#         except Exception as e:
#             return f"I encountered an error: {str(e)}"

#     def clear_memory(self):
#         """Reset conversation history — Jarvis forgets previous chat."""
#         self.conversation_history = []
#         return "Memory cleared. Starting fresh!"

# ============================================================
#  BRAIN MODULE
#  Connects to Claude AI (Anthropic API) OR Gemini (Google API)
#  This is the "intelligence" of Jarvis
# ============================================================

import config

# Optional imports depending on which provider you use
import anthropic
import google.generativeai as genai


class Brain:
    """
    The Brain can use either:
    1. Anthropic Claude API
    2. Google Gemini API

    Set in config.py:
        AI_PROVIDER = "anthropic"   # Use Claude
        AI_PROVIDER = "gemini"      # Use Gemini
    """

    def __init__(self):
        # Which provider to use?
        self.provider = getattr(config, "AI_PROVIDER", "anthropic").lower()

        # Conversation history for multi-turn chat
        self.conversation_history = []

        # Initialize selected AI provider
        if self.provider == "anthropic":
            self.client = anthropic.Anthropic(
                api_key=config.ANTHROPIC_API_KEY
            )
            print("🧠 AI Brain initialized with Claude (Anthropic)")

        elif self.provider == "gemini":
            # Configure Gemini
            genai.configure(api_key=config.GEMINI_API_KEY)

            # Create Gemini model instance
            self.model = genai.GenerativeModel(
                model_name=config.AI_MODEL,
                system_instruction=config.AI_SYSTEM_PROMPT
            )

            # Start a persistent chat session
            self.chat = self.model.start_chat(history=[])

            print("🧠 AI Brain initialized with Gemini (Google)")

        else:
            raise ValueError(
                "Invalid AI_PROVIDER. Use 'anthropic' or 'gemini'."
            )

    def ask(self, question: str) -> str:
        """
        Send a question to the selected AI provider and return the response.
        """

        # Save user's message in history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })

        # Keep only last 20 messages
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

        try:
            # ====================================================
            # CLAUDE (Anthropic)
            # ====================================================
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=config.AI_MODEL,
                    max_tokens=config.AI_MAX_TOKENS,
                    system=config.AI_SYSTEM_PROMPT,
                    messages=self.conversation_history
                )

                answer = response.content[0].text

            # ====================================================
            # GEMINI (Google)
            # ====================================================
            elif self.provider == "gemini":
                response = self.chat.send_message(question)

                # Extract plain text response
                answer = response.text

            else:
                return "Unsupported AI provider."

            # Save assistant response in history
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        # ========================================================
        # Anthropic Errors
        # ========================================================
        except anthropic.AuthenticationError:
            return "My Anthropic API key seems invalid."
        except anthropic.RateLimitError:
            return "Anthropic rate limit reached. Please wait a moment."

        # ========================================================
        # Generic Errors (works for Gemini too)
        # ========================================================
        except Exception as e:
            return f"I encountered an error: {str(e)}"

    def clear_memory(self):
        """
        Reset conversation history.
        """

        self.conversation_history = []

        # Reset Gemini chat session as well
        if self.provider == "gemini":
            self.chat = self.model.start_chat(history=[])

        return "Memory cleared. Starting fresh!"