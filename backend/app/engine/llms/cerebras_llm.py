"""
Cerebras LLM integration for LlamaIndex with Llama 4 Maverick support.
Ultra-fast inference with 2000+ tokens/sec.
"""

import os
from typing import Any, Callable, Optional, Sequence, Dict, List
from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseGen,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
    MessageRole,
)
from llama_index.core.llms import CustomLLM
from llama_index.core.llms.callbacks import llm_chat_callback, llm_completion_callback
from cerebras.cloud.sdk import Cerebras
import time


class CerebrasLLM(CustomLLM):
    """Cerebras LLM implementation for ultra-fast inference with Llama 4 Maverick."""

    model: str = "llama-4-maverick-17b-128e-instruct"
    temperature: float = 0.7
    max_tokens: int = 4096
    api_key: Optional[str] = None
    _client: Any = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        model: str = "llama-4-maverick-17b-128e-instruct",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.getenv("CEREBRAS_API_KEY")
        if not api_key:
            raise ValueError("CEREBRAS_API_KEY environment variable must be set")

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
            **kwargs
        )

        object.__setattr__(self, '_client', Cerebras(api_key=self.api_key))

    @property
    def client(self):
        return self._client

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=128000,  # Llama 4 Maverick's massive context window
            num_output=self.max_tokens,
            model_name=self.model,
            is_chat_model=True,
            is_function_calling_model=True,  # Llama 4 supports function calling
        )

    def _messages_to_cerebras_format(self, messages: Sequence[ChatMessage]) -> List[Dict[str, str]]:
        """Convert LlamaIndex messages to Cerebras format."""
        cerebras_messages = []
        for message in messages:
            role = message.role.value if hasattr(message.role, 'value') else str(message.role)
            cerebras_messages.append({
                "role": role,
                "content": message.content or ""
            })
        return cerebras_messages

    @llm_chat_callback()
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        """Chat with the model."""
        cerebras_messages = self._messages_to_cerebras_format(messages)

        start_time = time.time()

        response = self.client.chat.completions.create(
            messages=cerebras_messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )

        inference_time = time.time() - start_time

        # Calculate tokens per second for metrics
        if hasattr(response.usage, 'completion_tokens'):
            tokens_generated = response.usage.completion_tokens
            tokens_per_second = tokens_generated / inference_time if inference_time > 0 else 0
        else:
            tokens_per_second = 0

        return ChatResponse(
            message=ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response.choices[0].message.content,
            ),
            raw=response.model_dump(),
            additional_kwargs={
                "inference_time": inference_time,
                "tokens_per_second": tokens_per_second,
                "model": self.model
            }
        )

    @llm_chat_callback()
    def stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        """Stream chat responses."""
        cerebras_messages = self._messages_to_cerebras_format(messages)

        start_time = time.time()
        first_token_time = None
        tokens_count = 0

        response_stream = self.client.chat.completions.create(
            messages=cerebras_messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True,
            **kwargs
        )

        def gen() -> ChatResponseGen:
            nonlocal first_token_time, tokens_count
            content = ""

            for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    if first_token_time is None:
                        first_token_time = time.time()

                    delta = chunk.choices[0].delta.content
                    content += delta
                    tokens_count += 1

                    # Calculate time to first token and current tokens/sec
                    current_time = time.time()
                    ttft = first_token_time - start_time if first_token_time else 0
                    elapsed = current_time - first_token_time if first_token_time else 0
                    tps = tokens_count / elapsed if elapsed > 0 else 0

                    yield ChatResponse(
                        message=ChatMessage(
                            role=MessageRole.ASSISTANT,
                            content=content,
                        ),
                        delta=delta,
                        raw=chunk.model_dump() if hasattr(chunk, 'model_dump') else {},
                        additional_kwargs={
                            "time_to_first_token": ttft,
                            "tokens_per_second": tps,
                            "tokens_generated": tokens_count,
                            "model": self.model
                        }
                    )

        return gen()

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """Complete a prompt."""
        messages = [ChatMessage(role=MessageRole.USER, content=prompt)]
        response = self.chat(messages, **kwargs)
        return CompletionResponse(
            text=response.message.content,
            raw=response.raw,
            additional_kwargs=response.additional_kwargs
        )

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        """Stream completion."""
        messages = [ChatMessage(role=MessageRole.USER, content=prompt)]

        def gen() -> CompletionResponseGen:
            content = ""
            for response in self.stream_chat(messages, **kwargs):
                if response.delta:
                    content += response.delta
                    yield CompletionResponse(
                        text=content,
                        delta=response.delta,
                        raw=response.raw,
                        additional_kwargs=response.additional_kwargs
                    )

        return gen()
