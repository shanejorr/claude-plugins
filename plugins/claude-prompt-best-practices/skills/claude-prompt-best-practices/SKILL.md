---
name: claude-prompt-best-practices
description: "Reference guide for writing effective prompts for Claude. Use this skill whenever asked how to prompt Claude, how to write better prompts, prompt engineering tips, or how to get better results from Claude. Contains the full official Anthropic prompt engineering documentation covering general principles, formatting, tool use, thinking/reasoning, agentic systems, and model-specific tuning for Claude Opus 4.7, Sonnet 4.6, and Opus 4.6. Last fetched from docs.claude.com on 2026-04-24."
user-invocable: true
disable-model-invocation: true
---

# Claude Prompt Engineering Best Practices

> Source: Anthropic official documentation (fetched 2026-04-24)
> Pages:
> - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
> - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
> - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools

When this skill is invoked, read this document and use it to answer questions about prompt engineering for Claude. If the user asks about topics not covered here, note that the docs may have been updated and suggest they visit the URLs above.

---

## Claude Prompting Best Practices

### Model-Specific Tuning: Claude Opus 4.7

#### Response Length and Verbosity
Claude Opus 4.7 calibrates response length to task complexity — shorter for simple lookups, longer for open-ended analysis. If your product depends on a specific verbosity, tune your prompts explicitly. Positive examples showing the desired level of concision are more effective than negative examples or "don't do X" instructions.

#### Calibrating Effort and Thinking Depth
- **`xhigh` (new):** Best setting for most coding and agentic use cases.
- Effort is more important for this model than any prior Opus — experiment actively when you upgrade.
- If the model thinks more often than you'd like (common with large/complex system prompts), add guidance to steer it.
- If you see under-thinking at `medium`, raise effort first; then prompt for it directly if needed.

#### Tool Use Triggering
- Replace blanket defaults with targeted instructions: instead of "Default to using [tool]," use "Use [tool] when it would enhance your understanding of the problem."
- Remove over-prompting. Tools that under-triggered in older models now trigger appropriately. Instructions like "If in doubt, use [tool]" will cause over-triggering.

#### User-Facing Progress Updates
Opus 4.7 provides more regular, higher-quality progress updates during long agentic traces. If you've added scaffolding to force status messages, try removing it. If updates are poorly calibrated, describe what they should look like and provide examples.

#### More Literal Instruction Following
Opus 4.7 follows instructions more literally. Review prompts that relied on Claude inferring intent beyond what was literally stated.

#### Tone and Writing Style
Opus 4.7 is more direct and opinionated, with less validation-forward phrasing and fewer emoji than Opus 4.6's warmer style. If your product relies on a specific voice, re-evaluate style prompts against the new baseline.

#### Controlling Subagent Spawning
Opus 4.7 tends to spawn fewer subagents by default. Steer this behavior explicitly. Example:

```
Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see).

Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.
```

#### Design and Frontend Defaults
Opus 4.7 defaults to a specific visual aesthetic. Generic instructions shift it to a different fixed palette rather than producing variety. Two approaches that work reliably:

**1. Specify a concrete alternative** with explicit color palette, typography, layout, and component specs.

**2. Have the model propose options before building.** This breaks the default and gives users control.

Short-form prompt option:
```
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

#### Computer Use
Works across resolutions up to 2576px / 3.75MP. Sending images at 1080p provides a good balance of performance and cost. For cost-sensitive workloads, 720p or 1366×768 are solid lower-cost options.

---

### General Principles

#### Be Clear and Direct
Claude responds well to clear, explicit instructions. Think of Claude as a brilliant but new employee who lacks context on your norms.

**Golden rule:** Show your prompt to a colleague with minimal context. If they'd be confused, Claude will be too.

- Be specific about the desired output format and constraints.
- Use numbered lists or bullet points when order or completeness of steps matters.

#### Add Context to Improve Performance
Explain *why* an instruction matters. Claude is smart enough to generalize from the explanation and deliver more targeted responses.

#### Use Examples Effectively (Few-Shot / Multishot Prompting)
Examples are one of the most reliable ways to steer format, tone, and structure. Make them:
- **Relevant:** Mirror your actual use case closely.
- **Diverse:** Cover edge cases and vary enough that Claude doesn't pick up unintended patterns.
- **Clear:** Label expected outputs so Claude understands the structure.

#### Structure Prompts with XML Tags
XML tags help separate different parts of your prompt. Best practices:
- Use consistent, descriptive tag names.
- Nest tags logically for hierarchical content.
- Reference tag names in your instructions.

#### Give Claude a Role
Setting a role in the system prompt focuses Claude's behavior and tone. Even a single sentence makes a difference:

```python
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    system="You are a helpful coding assistant specializing in Python.",
    messages=[{"role": "user", "content": "Write a function to sort a list."}],
)
```

#### Long Context Prompting (20k+ tokens)
- **Put longform data at the top:** Place documents and inputs near the top of your prompt, above your query, instructions, and examples.
- **Ask Claude to quote first:** For document Q&A, instruct Claude to find relevant quotes before answering.
- **Ground responses in quotes:** For long document tasks, ask Claude to quote relevant parts before carrying out its task.

#### Model Self-Knowledge
If you want Claude to identify itself correctly or use specific API strings, provide that information directly in the system prompt.

---

### Output and Formatting

#### Communication Style
Claude's latest models are more concise and natural compared to previous models — more direct, conversational, and less verbose. Claude may skip verbal summaries after tool calls and jump directly to the next action. If you prefer more visibility into its reasoning, add: "After each tool call, briefly summarize what you found and what you plan to do next."

#### Control the Format of Responses

1. **Tell Claude what to do instead of what not to do**
   - Instead of: "Do not use markdown in your response"
   - Try: "Your response should be composed of smoothly flowing prose paragraphs."

2. **Use XML format indicators**
   - Try: "Write the prose sections of your response in `<smoothly_flowing_prose_paragraphs>` tags."

3. **Match your prompt style to the desired output** — removing markdown from your prompt can reduce markdown in the output.

4. **Use detailed prompts for specific formatting preferences:**

```
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form content, write in clear, flowing prose using complete paragraphs and sentences. Use standard paragraph breaks for organization and reserve markdown primarily for `inline code`, code blocks, and simple headings. Avoid using **bold** and *italics*.

DO NOT use ordered lists or unordered lists unless: a) you're presenting truly discrete items where a list format is the best option, or b) the user explicitly requests a list or ranking.

Instead of listing items with bullets or numbers, incorporate them naturally into sentences. NEVER output a series of overly short bullet points.
</avoid_excessive_markdown_and_bullet_points>
```

#### LaTeX Output
Claude Opus 4.6 defaults to LaTeX for mathematical expressions. To disable: "Do not use LaTeX formatting for mathematical expressions. Use plain text notation instead."

#### Migrating Away from Prefilled Responses
Prefilled responses on the last assistant turn are deprecated starting with Claude 4.6 models:
- Move format guidance from prefills into explicit system prompt instructions.
- Use XML tags to structure expected output sections.
- Use role-setting and examples to achieve the tone/format the prefill was targeting.

---

### Tool Use

#### Be Explicit About Action vs. Suggestion
Claude's latest models benefit from explicit direction to use specific tools. "Can you suggest some changes" may produce suggestions instead of implementations.

To make Claude more proactive by default:
```
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is unclear, infer the most useful likely action and proceed, using tools to discover any missing details instead of guessing.
</default_to_action>
```

To make Claude more hesitant (only act if explicitly requested):
```
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed to make changes. When the user's intent is ambiguous, default to providing information, doing research, and providing recommendations rather than taking action.
</do_not_act_before_instructions>
```

**Note:** If your prompts were designed to reduce under-triggering in older models, dial back aggressive language for Claude 4.5/4.6+. Replace "CRITICAL: You MUST use this tool when..." with "Use this tool when...".

#### Optimize Parallel Tool Calling
Claude's latest models excel at parallel tool execution — multiple searches, reading several files at once, parallel bash commands. To maximize this:

```
<maximize_parallel_efficiency>
Maximize efficiency by using tools in parallel wherever possible. When you need information from multiple sources, request them simultaneously rather than sequentially. Always think about which operations can be parallelized before executing.
</maximize_parallel_efficiency>
```

---

### Thinking and Reasoning

#### Overthinking and Excessive Thoroughness
If Claude Opus 4.6 overthinks tasks:
- Replace blanket defaults with targeted instructions.
- Remove over-prompting on tools.
- Lower the `effort` setting.
- Add explicit constraints: "Only use extended thinking for tasks that genuinely require it, such as complex math, nuanced analysis, or multi-step planning. For straightforward questions, respond directly without thinking."

#### Leverage Adaptive Thinking
Use adaptive thinking for agentic behavior — multi-step tool use, complex coding, long-horizon agent loops.

Guide Claude's thinking:
```
Before beginning complex tasks, briefly think through your approach. After each significant tool result, reflect on what you've learned and whether your plan needs to change.
```

If the model thinks too often:
```
Only use extended thinking when the task genuinely requires deep reasoning. For simple requests and lookups, respond immediately without extended thinking.
```

#### Migrating from `budget_tokens` to Adaptive Thinking

**Before (older models):**
```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "..."}]
)
```

**After (adaptive thinking):**
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=64000,
    effort="medium",
    messages=[{"role": "user", "content": "..."}]
)
```

---

### Agentic Systems

#### Context Awareness and Multi-Window Workflows
Claude 4.6 and 4.5 models feature context awareness, enabling them to track their remaining context window throughout a conversation.

If your harness compacts context automatically, add this so Claude doesn't try to artificially wrap up:
```
You are operating in an environment that automatically compacts your context when it gets full. Don't worry about context limits — focus on completing the task thoroughly.
```

#### Multi-Context Window Workflows
1. Use the first context window to set up a framework (write tests, create setup scripts), then iterate with a todo-list in future windows.
2. Maintain structured progress files (e.g., `progress.txt`) updated at each step.
3. Create setup scripts (e.g., `init.sh`) to gracefully start servers and run test suites.
4. When starting fresh: "Review progress.txt, tests.json, and the git logs."
5. Use verification tools (Playwright MCP, computer use) for autonomous testing.

#### State Management Best Practices
- Use structured formats (JSON) for tracking structured data like test results.
- Use unstructured text for freeform progress notes.
- Explicitly ask Claude to keep track of incremental progress.

#### Balancing Autonomy and Safety
To require confirmation before risky actions:
```
<confirm_before_risky_actions>
Examples of actions that warrant confirmation:
- Destructive operations: deleting files or branches, dropping database tables, rm -rf
- Hard to reverse operations: git push --force, git reset --hard, amending published commits
- Operations visible to others: pushing code, commenting on PRs/issues, sending messages, modifying shared infrastructure

When encountering obstacles, do not use destructive actions as a shortcut.
</confirm_before_risky_actions>
```

#### Research and Information Gathering
Structured 5-step research approach:
```
<research_approach>
[Research task]

Step 1: Search broadly to identify the most relevant sources.
Step 2: Deep dive into the top 3-5 sources.
Step 3: Cross-reference findings across sources.
Step 4: Critique your own findings — what's uncertain, what's missing?
Step 5: Synthesize into a final answer with citations.
</research_approach>
```

#### Subagent Orchestration
Claude's latest models proactively delegate to subagents. To take advantage:
- Ensure well-defined subagent tools in tool definitions.
- Describe what each subagent specializes in.

To constrain excessive subagent use:
```
<subagent_usage>
Only spawn subagents for tasks that require specialized capabilities or parallel execution. Don't create a subagent for work you can complete directly and quickly yourself.
</subagent_usage>
```

#### Prompt Chaining
Still useful when you need to inspect intermediate outputs or enforce a specific pipeline. The most common pattern is **self-correction:** generate a draft → review it → refine based on review. Each step is a separate API call so you can log, evaluate, or branch.

#### Reduce File Creation
If you prefer to minimize temporary file creation:
```
After completing your work, clean up any temporary files you created during your process. Only keep files that are part of the final deliverable.
```

#### Prevent Overeagerness / Overengineering
```
<minimal_implementation>
- Scope: Don't add features, refactor code, or make "improvements" beyond what was asked.
- Documentation: Don't add docstrings, comments, or type annotations to code you didn't change.
- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios that can't happen.
- Abstractions: Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements.
</minimal_implementation>
```

#### Avoid Overfitting to Tests / Hard-Coding
```
Focus on understanding the problem requirements and implementing the correct algorithm. Tests are there to verify correctness, not to define the solution. If the task is unreasonable or infeasible, or if any of the tests are incorrect, please inform me rather than working around them.
```

#### Minimize Hallucinations in Agentic Coding
```
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating unless you are certain of the correct answer.
</investigate_before_answering>
```

---

### Capability-Specific Tips

#### Vision
Claude Opus 4.5 and 4.6 have improved vision capabilities. Analyze videos by breaking them into frames.

#### Frontend Design
To avoid the "AI slop" aesthetic with Claude 4.5/4.6:
```
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- Motion: Use animations for effects and micro-interactions. Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character
</frontend_aesthetics>
```

---

### Migration Considerations

#### Migrating to Claude 4.6 Models
- Be specific about desired behavior.
- Add modifiers encouraging quality: instead of "Create an analytics dashboard," use "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."
- Request animations and interactive elements explicitly.
- Migrate away from prefilled responses (deprecated in 4.6+).
- **Dial back anti-laziness prompting** — Claude 4.6 is significantly more proactive and may over-trigger on aggressive prompting.

#### Migrating to Claude Sonnet 4.6

Sonnet 4.6 defaults to `effort="high"` (Sonnet 4.5 had no effort parameter).

**Recommended effort settings:**
- `medium` for most applications
- `low` for high-volume or latency-sensitive workloads
- Set max output tokens to 64k at medium or high effort

**For coding use cases:**
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    effort="medium",
    messages=[{"role": "user", "content": "..."}]
)
```

**For chat and non-coding use cases:**
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    effort="low",
    messages=[{"role": "user", "content": "..."}]
)
```

**When to use Opus 4.7 instead:** For the hardest, longest-horizon problems — large-scale code migrations, deep research, extended autonomous work.