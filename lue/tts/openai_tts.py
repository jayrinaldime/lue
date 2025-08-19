import logging
from rich.console import Console

from .base import TTSBase
import config
import os

class OpenAITTS(TTSBase):
    """TTS implementation for Microsoft Edge's online TTS service."""

    @property
    def name(self) -> str:
        return "openai"

    @property
    def output_format(self) -> str:
        return "mp3"

    def __init__(self, console: Console, voice: str = None, lang: str = None):
        super().__init__(console, voice, lang)
        self.openai_tts = None
        if self.voice is None:
            self.voice = config.TTS_VOICES.get(self.name)

    async def initialize(self) -> bool:
        """Checks if the openai library is available."""
        try:
            from openai import AsyncOpenAI
            self.openai_tts = AsyncOpenAI()
            self.initialized = True
            self.console.print("[green]openai model is available.[/green]")
            return True
        except ImportError:
            self.console.print("[bold red]Error: 'openai' package not found.[/bold red]")
            self.console.print("[yellow]Please run 'pip install openai' to use this TTS model.[/yellow]")
            logging.error("'OpenAI' is not installed.")
            return False

    async def generate_audio(self, text: str, output_path: str):
        """Generates audio from text using openai and saves it to a file."""
        if not self.initialized:
            raise RuntimeError("openai has not been initialized.")
        try:

            response = await self.openai_tts.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=self.voice,
                input=text,
                response_format="mp3",
            )

            # Stream the audio response directly to the file
            response.stream_to_file(output_path)

        except Exception as e:
            logging.error(f"OpenAI TTS audio generation failed for text: '{text[:50]}...'", exc_info=True)
            raise e

    async def warm_up(self):
        pass