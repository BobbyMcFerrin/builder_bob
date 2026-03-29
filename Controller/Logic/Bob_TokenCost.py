######################################################
# Bob Token Cost Predictor
#
# Predicts token cost for structured JSON + input
# calls to OpenAI API
######################################################

import json


def predict_token_cost(messages, response_format=None, model='gpt-4o'):
    """
    Predict token cost for a structured JSON + input call to OpenAI API.

    :param messages: List of message dicts (role/content) or a single string
    :param response_format: Pydantic BaseModel class for structured output (optional)
    :param model: Model name (default: 'gpt-4o')
    :return: Dict with token estimates and cost prediction
    """
    # Model pricing per 1K tokens (as of 2024)
    MODEL_PRICING = {
        'gpt-4o': {'input': 0.005, 'output': 0.015},
        'gpt-4o-mini': {'input': 0.00015, 'output': 0.0006},
        'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
        'gpt-5.2': {'input': 0.005, 'output': 0.015},  # Assuming similar to gpt-4o
    }

    def estimate_tokens(text):
        """Estimate tokens using character-based heuristic (avg ~4 chars per token)"""
        if not text:
            return 0
        # Hebrew text tends to have higher token-per-char ratio
        char_count = len(text)
        # Check for Hebrew characters
        hebrew_chars = sum(1 for c in text if '\u0590' <= c <= '\u05FF')
        hebrew_ratio = hebrew_chars / max(char_count, 1)
        # Adjust ratio: Hebrew ~2-3 chars/token, English ~4 chars/token
        avg_chars_per_token = 2.5 if hebrew_ratio > 0.3 else 4
        return int(char_count / avg_chars_per_token)

    def estimate_schema_tokens(pydantic_model):
        """Estimate tokens for Pydantic schema serialization"""
        if pydantic_model is None:
            return 0
        try:
            schema = pydantic_model.model_json_schema()
            schema_str = json.dumps(schema, ensure_ascii=False)
            return estimate_tokens(schema_str)
        except Exception:
            return 100  # Default fallback

    def estimate_output_tokens(pydantic_model):
        """Estimate expected output tokens based on schema structure"""
        if pydantic_model is None:
            return 500  # Default for unstructured output
        try:
            schema = pydantic_model.model_json_schema()
            properties = schema.get('properties', {})

            total_tokens = 50  # Base JSON structure overhead

            for field_name, field_info in properties.items():
                field_type = field_info.get('type', '')

                if field_type == 'string':
                    total_tokens += 50  # Average string field
                elif field_type == 'array':
                    items = field_info.get('items', {})
                    if '$ref' in items or items.get('type') == 'string':
                        total_tokens += 100  # Array of enums/strings
                    else:
                        total_tokens += 200  # Complex array
                elif field_type == 'boolean':
                    total_tokens += 5
                elif field_type == 'integer' or field_type == 'number':
                    total_tokens += 10
                elif field_type == 'object':
                    total_tokens += 100
                else:
                    total_tokens += 30  # Default

            return total_tokens
        except Exception:
            return 200  # Default fallback

    # Calculate input tokens
    input_tokens = 0

    if isinstance(messages, str):
        input_tokens = estimate_tokens(messages)
    elif isinstance(messages, list):
        for msg in messages:
            if isinstance(msg, dict):
                content = msg.get('content', '')
                if isinstance(content, str):
                    input_tokens += estimate_tokens(content)
                elif isinstance(content, list):
                    # Handle multimodal content (text + images)
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                input_tokens += estimate_tokens(item.get('text', ''))
                            elif item.get('type') == 'image_url':
                                # Images have fixed token costs based on detail level
                                detail = item.get('image_url', {}).get('detail', 'auto')
                                if detail == 'high':
                                    input_tokens += 765  # High detail image
                                else:
                                    input_tokens += 85   # Low detail image

    # Add schema tokens (sent as part of the request)
    schema_tokens = estimate_schema_tokens(response_format)
    input_tokens += schema_tokens

    # Estimate output tokens
    output_tokens = estimate_output_tokens(response_format)

    # Get pricing
    pricing = MODEL_PRICING.get(model, MODEL_PRICING['gpt-4o'])

    # Calculate costs
    input_cost = (input_tokens / 1000) * pricing['input']
    output_cost = (output_tokens / 1000) * pricing['output']
    total_cost = input_cost + output_cost

    return {
        'model': model,
        'input_tokens': input_tokens,
        'schema_tokens': schema_tokens,
        'estimated_output_tokens': output_tokens,
        'total_estimated_tokens': input_tokens + output_tokens,
        'input_cost_usd': round(input_cost, 6),
        'output_cost_usd': round(output_cost, 6),
        'total_cost_usd': round(total_cost, 6),
        'pricing_per_1k': pricing
    }
