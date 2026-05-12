# ============================================================
#  BRAIN MODULE
#  Connects to Claude AI (Anthropic API) to answer questions
#  This is the "intelligence" of Jarvis
# ============================================================

import anthropic
import config

class Brain:
    """
    The Brain uses the Anthropic Claude API to answer any question
    that isn't handled by a specific command module.
    
    CONCEPT: Large Language Models (LLMs)
    Claude is an LLM — a neural network trained on massive amounts of text.
    It predicts the most likely next token (word piece) given your input.
    The result feels like "understanding" because it has learned patterns
    from billions of documents about how conversations, facts, and 
    reasoning work.
    
    CONCEPT: API (Application Programming Interface)
    An API is a way for your code to talk to someone else's service.
    We send: your question (as JSON over HTTPS)
    We receive: Claude's answer (as JSON)
    We pay: per token (input tokens + output tokens)
    
    CONCEPT: Tokens
    Text is split into tokens (roughly 3/4 of a word).
    "Hello world" = 2 tokens
    "Artificial intelligence" = 3 tokens
    Pricing and context limits are measured in tokens.
    """

    def __init__(self):
        # Create Anthropic client — handles authentication and HTTP
        # It automatically reads ANTHROPIC_API_KEY from environment
        # or you can pass it explicitly as shown below
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
        # Conversation history — enables multi-turn conversations
        # Each item: {"role": "user"/"assistant", "content": "text"}
        self.conversation_history = []
        
        print("🧠 AI Brain initialized")

    def ask(self, question: str) -> str:
        """
        Send a question to Claude and get a response.
        
        CONCEPT: Messages API
        Claude uses a "messages" format (like chat):
        - "user" messages = what you say
        - "assistant" messages = what Claude says
        - "system" message = instructions that always apply
        
        CONCEPT: Context Window
        Claude remembers the full conversation_history each API call.
        This is why it can remember what you said 3 messages ago.
        But there's a limit (200k tokens for Claude) — very old messages
        eventually need to be dropped (we handle this below).
        """
        # Add the new question to history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })
        
        # Keep history manageable — last 20 messages only
        # This prevents hitting context limits and saves API costs
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        try:
            # Make the API call
            response = self.client.messages.create(
                model=config.AI_MODEL,
                max_tokens=config.AI_MAX_TOKENS,
                
                # System prompt = Jarvis's personality & instructions
                # This is NOT part of conversation_history — it's separate
                system=config.AI_SYSTEM_PROMPT,
                
                # Send full conversation so Claude has context
                messages=self.conversation_history
            )
            
            # Extract the text from the response
            # response.content is a list of ContentBlock objects
            # We want the text from the first (usually only) block
            answer = response.content[0].text
            
            # Add Claude's response to history for next turn
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })
            
            return answer
            
        except anthropic.AuthenticationError:
            return "My API key seems invalid. Please check the config file."
        except anthropic.RateLimitError:
            return "I'm being rate limited. Please wait a moment."
        except Exception as e:
            return f"I encountered an error: {str(e)}"

    def clear_memory(self):
        """Reset conversation history — Jarvis forgets previous chat."""
        self.conversation_history = []
        return "Memory cleared. Starting fresh!"