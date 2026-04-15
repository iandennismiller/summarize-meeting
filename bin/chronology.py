#!/usr/bin/env python3

import argparse

from openai import OpenAI


def create_openai_client(base_url: str, api_key: str = "local-api-key") -> OpenAI:
    """Create a client for a local OpenAI-compatible endpoint."""
    return OpenAI(base_url=base_url, api_key=api_key)


def ensure_chat_model_available(client: OpenAI, model_name: str) -> None:
    """Validate endpoint connectivity and model availability when listed by the endpoint."""
    try:
        model_list = client.models.list()
    except Exception as exc:
        raise RuntimeError("Could not connect to the configured OpenAI-compatible endpoint.") from exc

    model_ids = {model.id for model in model_list.data if getattr(model, "id", None)}
    if model_ids and model_name not in model_ids:
        available = ", ".join(sorted(model_ids))
        raise RuntimeError(f"Configured model '{model_name}' is not available. Endpoint models: {available}")

def summarize_transcript(
    transcript: str,
    client: OpenAI,
    llm_model: str = "qwen3.5:4b",
    timeout_seconds: int = 600,
) -> str:
    """Generate a meeting chronology summary from the transcript using the specified LLM model.
    
    Increase `timeout_seconds` for longer transcripts or slower local hardware.
    """
    prompt = f"""<System>
Act as a professional minute-taker. Please analyze the following meeting transcript and generate a strict chronological timeline of events.

Requirements:

- Structure the output as a table: [Time/Order] | [Event/Topic] | [Key Details].
- Estimate the time for each topic based on how many words are spent discussing it, assuming an average speaking rate of 60 words per minute.
- Keep descriptions concise and factual.
</System>

<User Input>
Here is the transcript for analysis:

{transcript}
</User Input>
"""

    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {"role": "system", "content": "You summarize meeting transcripts."},
            {"role": "user", "content": prompt},
        ],
        timeout=timeout_seconds,
    )

    summary = (response.choices[0].message.content or "").strip()
    if not summary:
        raise RuntimeError("LLM returned an empty summary.")
    return summary

def main():
    parser = argparse.ArgumentParser(description="Summarize a meeting transcript using a local OpenAI-compatible endpoint.")
    parser.add_argument("--endpoint", type=str, default="http://localhost:8000/v1", help="Base URL of the OpenAI-compatible endpoint")
    parser.add_argument("--model", type=str, default="qwen3.5:4b", help="LLM model to use for summarization")
    parser.add_argument("--input-file", type=str, required=True, help="Path to the transcript text file")
    parser.add_argument("--output-file", type=str, required=True, help="Path to save the summary output")
    args = parser.parse_args()

    client = create_openai_client(base_url=args.endpoint)
    ensure_chat_model_available(client, args.model)

    with open(args.input_file, "r") as f:
        transcript = f.read()

    summary = summarize_transcript(transcript, client, llm_model=args.model)

    with open(args.output_file, "w") as f:
        f.write(summary)

main()
