import os
import ollama
from openai import OpenAI
from helpers.logger import setup_logger
from integrations.memory import AgentMemory

LLM_API_KEY = os.getenv("OPENAI_API_KEY")


class LLMClient:
    def __init__(self, config):
        self.logger = setup_logger("app")
        self.llm_config = config.get("llm_config", {})
        self.api_key = LLM_API_KEY

        self.provider = self.llm_config.get("provider", "openai")
        self.model = self.llm_config.get("model", "gpt-4o")
        self.temperature = self.llm_config.get("temperature", 0.7)
        self.context_window = self.llm_config.get("context_window", 10000)

        self.include_history = self.llm_config.get("include_history", False)
        self.history_length = self.llm_config.get("history_length", 10)
        self.behavior = self.llm_config.get("chatbot_behavior", {})  # TODO add behavior to config

        self.client = self._initialize_client()

    def _initialize_client(self):
        if self.provider == "openai":
            if not self.api_key or self.api_key == "<YOUR_API_KEY_HERE>":
                self.logger.error("Missing OpenAI API key.")
                raise ValueError("Missing OpenAI API key.")
            return OpenAI(api_key=self.api_key)
        return None

    def _describe_chatbot_behavior(self):
        return "\n".join([
            f"{key.replace('_', ' ').capitalize()}: {value}"
            for key, value in self.behavior.items()
        ])

    def ask(self, user_input=None,
            system_prompt=None,
            model=None, temperature=None,
            include_history=None):

        model = model or self.model
        temperature = temperature or self.temperature
        include_history = include_history or self.include_history

        messages = [{"role": "system", "content": self._describe_chatbot_behavior()}]
        if system_prompt: messages.append([{"role": "system", "content": system_prompt}])
        if user_input: messages.append({"role": "user", "content": user_input})

        if include_history:
            messages.extend(AgentMemory().get_history(limit=self.history_length))

        self.logger.info(f"Calling LLM ({self.provider}, model: {model}) with prompt: {user_input}")
        self.logger.debug(f"Full prompt: {messages}")

        provider_handlers = {
            "openai": lambda: self._openai_call(messages, model, temperature),
            "ollama": lambda: self._ollama_call(messages, model)
        }

        handler = provider_handlers.get(self.provider)
        if handler:
            return handler()
        else:
            self.logger.error(f"Unsupported LLM provider: {self.provider}")
            return "Error: Unsupported LLM provider."

    def _openai_call(self, messages, model, temperature):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=self.context_window,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return "Error: Failed OpenAI request."

    def _ollama_call(self, messages, model):
        try:
            response = ollama.chat(model=model, messages=messages)
            return response["message"]["content"].strip()
        except Exception as e:
            self.logger.error(f"Ollama API error: {e}")
            return "Error: Failed Ollama request."
