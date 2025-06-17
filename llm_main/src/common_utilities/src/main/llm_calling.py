import os
from typing import Optional, Dict, Any
from enum import Enum
from abc import ABC, abstractmethod
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
import os
import dotenv
import re
import json
import re
from constants import model_name


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ModelProvider(Enum):
    """Enum for supported LLM providers"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    
class ModelConfig:
    """Constants for model configurations"""
    MODEL_CONFIGS = {
        #Genimi models
        "gemini": {
            "version": "gemini-2.5-flash-preview-05-20",
            "api_key_env": "api_key_ge_2_5",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "provider": ModelProvider.GEMINI,
        },
        
        # OpenAI models
        "openai": {
            "version": "gpt-4.1-nano-2025-04-14",
            "api_key_env": "open_ai_key",
            "base_url": "",
            "provider": ModelProvider.OPENAI,
        },
        
        # DeepSeek models
        "deepseek": {
            "version": "deepseek-chat",
            "api_key_env": "deep_seek_api",
            "base_url": "https://api.deepseek.com",
            "provider": ModelProvider.DEEPSEEK,
        }
    }

class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        pass

class OpenAIClient(LLMClient):
    """Client for OpenAI-based models"""
    
    def __init__(self, api_key: str, base_url: str, model: str):
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                # temperature=1.0,
                # max_tokens=2048,
                # top_p=1.0
            )
            response_text = response.choices[0].message.content
            print('response_text >>>', response_text)
            processor = PostProcessing(response_text)
            # Get the formatted response
            result = processor.get_formatted_response()
            return result
        
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise



class PostProcessing:
    """Class to process and extract JSON from response text."""
    
    def __init__(self, response_text: str):
        """
        Initialize the PostProcessing class with the response text.

        Args:
            response_text (str): The text response containing potential JSON data.
        """
        self.response_text = response_text
        self.formatted_response: Dict[Any, Any] = self.extract_and_save_json()
    
    def extract_and_save_json(self, output_filename: Optional[str] = None) -> Dict[Any, Any]:
        """
        Extract JSON from the response text using regex patterns and optionally save to a file.

        Args:
            output_filename (Optional[str]): Name of the output JSON file (without extension).
                                           If None, no file is saved.

        Returns:
            Dict[Any, Any]: The extracted JSON data as a dictionary.
                           Returns an error dictionary if no valid JSON is found.
        """
        # Define regex patterns for extracting JSON content
        patterns = [
            r'```json\s*(\{[\s\S]*?\})\s*```',  # Code block with json
            r"'''json\s*(\{[\s\S]*?\})\s*'''",  # Triple quotes with json
            r'<json response>\s*(\{[\s\S]*?\})\s*</json response>',  # XML-like tags
            r'\*\*<json response>\*\*\s*(\{[\s\S]*?\})\s*\*\*<json response>\*\*',  # Markdown bold tags
            r'```<json response>\s*(\{[\s\S]*?\})\s*```',  # Code block with json response
            r"'''<json response>\s*(\{[\s\S]*?\})\s*'''"  # Triple quotes with json response
        ]

        extracted_data: Dict[Any, Any] = {"error": "No valid JSON found in response"}

        # Try to extract JSON content using regex patterns
        for pattern in patterns:
            try:
                logger.debug(f"Trying pattern: {pattern}")
                match = re.search(pattern, self.response_text, re.DOTALL)
                if match:
                    json_str = match.group(1).strip()
                    try:
                        extracted_data = json.loads(json_str)
                        logger.info("Successfully extracted JSON from response")
                        break
                    except json.JSONDecodeError as e:
                        logger.warning(f"Invalid JSON format with pattern {pattern}: {str(e)}")
                        continue
            except re.error as e:
                logger.error(f"Regex error with pattern {pattern}: {str(e)}")
                continue

        # Save to file if output_filename is provided
        if output_filename:
            try:
                filename = f"{output_filename}.json" if not output_filename.endswith('.json') else output_filename
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(extracted_data, f, indent=2)
                logger.info(f"Saved JSON to {filename}")
            except IOError as e:
                logger.error(f"Failed to save JSON to {filename}: {str(e)}")

        return extracted_data

    def get_formatted_response(self) -> Dict[Any, Any]:
        """
        Get the formatted response extracted during initialization.

        Returns:
            Dict[Any, Any]: The extracted JSON data as a dictionary.
        """
        return self.formatted_response


class LLMFactory:
    """Factory to create appropriate LLM client based on model name"""
    
    @staticmethod
    def get_client(model_name: str) -> LLMClient:
        if model_name not in ModelConfig.MODEL_CONFIGS:
            raise ValueError(f"Unsupported model: {model_name}")
            
        config = ModelConfig.MODEL_CONFIGS[model_name]
        dotenv.load_dotenv()
        api_key = os.getenv(config["api_key_env"])
        model_version = config["version"]
        base_url = config["base_url"]
        print('model_name >>>', model_name, '|| model_version >>>', model_version)
        if not api_key:
            raise ValueError(f"API key not found in environment variable: {config['api_key_env']}")
            
        provider = config["provider"]
        
        if provider == ModelProvider.OPENAI:
            return OpenAIClient(
                api_key=api_key,
                base_url=None,
                model=model_version
            )
        
        else:
            return OpenAIClient(
                api_key=api_key,
                base_url=base_url,
                model=model_version
            )




if __name__ == "__main__":
    llm_client = LLMFactory.get_client(model_name)
    prompt="Explain how AI works in a few words in 200 words?",
    sys_prompt="You are a helpful assistant providing concise answers"
    response = llm_client.generate_response(str(sys_prompt), str(prompt))
    print(response)