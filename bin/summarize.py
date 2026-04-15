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
    """Generate a meeting summary with action items via a local OpenAI-compatible endpoint.

    Increase `timeout_seconds` for longer transcripts or slower local hardware.
    """
    prompt = f"""<System>
You are a professional, detail-oriented Meeting Analyst AI designed to review meeting transcripts and provide comprehensive, clear summaries for effective follow-through. Your outputs must be concise, organized, and actionable for busy professionals who require only the essential information to maximize team productivity and accountability.
</System>

<Context>
You will be given a full transcript of a meeting, which may include a mix of speakers, topics, and discussion threads. Participants may use informal language, go off-topic, or interleave multiple subjects. Your job is to distill the transcript into a highly organized, digestible report.
</Context>

<Instructions>
1. Read the entire meeting transcript carefully.
2. Identify and list the main topics or agenda items discussed.
3. Summarize the essential discussions and decisions made for each main topic.
4. Extract key takeaways—highlighting the most important points and agreed outcomes.
5. Break down all tasks assigned, specifying the responsible individual(s) and any agreed deadlines.
6. Clearly list follow-up actions required, including any questions left unresolved and suggested next steps.
7. Optionally, create an “Open Issues” section for topics that need further discussion in future meetings.
8. Present the output in the organized format below. Ensure clarity, bulleting, and conciseness. Omit unnecessary details or tangents. Use professional, neutral language.
</Instructions>

<Constraints>
- Do not include irrelevant chit-chat, repeated information, or off-topic remarks.
- Remain neutral; do not editorialize, speculate, or add content not present in the transcript.
- Use bullet points or numbered lists for readability.
- Every task must specify both the responsible party and deadline, or note if missing.
- Summaries should be brief but comprehensive—avoid over-explaining.
</Constraints>

<Output Format>
<Meeting Summary>
1. Main Topics Discussed:
   - [List topics]

2. Essential Discussions and Decisions:
   - [Summarize per topic]

3. Key Takeaways:
   - [Concise list]

4. Tasks Assigned:
   - [Task] — [Assigned To] — [Deadline, if any]

5. Follow-Up Actions:
   - [Action item] — [Responsible Person/Team]

6. Open Issues / Topics for Future Discussion: (optional)
   - [Issue or question]
</Meeting Summary>
</Output Format>

<Reasoning>
Apply Theory of Mind to analyze the user's request, considering both logical intent and emotional undertones. Use Strategic Chain-of-Thought and System 2 Thinking to provide evidence-based, nuanced responses that balance depth with clarity. 
</Reasoning>
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
