**Architecture**
- `agent.py` pairs `AgentContext` (task orchestration, chat persistence via `python/helpers/defer.DeferredTask`) with `Agent` instances that communicate up/down a hierarchy through `_process_chain`.
- The message loop in `Agent.monologue` runs ordered extension hooks from `python/extensions/<stage>/`; name new hooks with numeric prefixes to control sequencing.
- Prompts live in `prompts/default`; `agent.system.main.md` stitches together other files and custom overrides are selected through `AgentConfig.prompts_subdir` (see `initialize.py`).
- Tools are auto-discovered from `python/tools/*.py` via `python/helpers/extract_tools.load_classes_from_folder`; pair each tool class with a prompt snippet referenced in `prompts/default/agent.system.tools.md`.

**Tool Calls & Messaging**
- Model replies must expose the first JSON object as `{"tool_name": ..., "tool_args": {...}}`; `Agent.process_tools` only inspects that block and rejects misformatted text.
- Use `tool_name` patterns like `scheduler:run_task` to map onto `Tool.method`; subclasses set behavior through `python/helpers/tool.Tool`.
- `code_execution_tool.py` spins SSH sessions (or Docker if enabled) keyed by `session` id and keeps state under `_cet_state`; expect commands to run in `work_dir`.
- `python/tools/scheduler.py` wraps `python/helpers/task_scheduler` models; long-running task kicks must set `Response.break_loop=True` if the same context will continue the conversation.

**Runtime & APIs**
- Run `python prepare.py` once to seed the root SSH password (`tmp/settings.json`), then launch the stack with `python run_ui.py --port 50001` (loads `.env`, starts Flask UI, job loop, and optional Cloudflare tunnel).
- API endpoints auto-register from `python/api/*.py`; each `ApiHandler` subclass can demand auth, loopback, or API key, and gets contexts through `AgentContext` helpers.
- The scheduler tick runs every 60s via `python/helpers/job_loop.run_loop`; keep new background work async-friendly to avoid blocking the loop.
- Development mode toggles come from `python/helpers/runtime` args (`--cloudflare_tunnel`, `--port`, `--development`) and propagate through `initialize.py` overrides.

**State & Storage**
- User settings persist in `tmp/settings.json` managed by `python/helpers/settings`; secrets live in `.env` (see `example.env`).
- Chat logs stream to `logs/*.html`; working artifacts land in `work_dir`; knowledge ingestion drops files into `knowledge/custom/main` for the RAG pipeline.
- Behavior adjustments are merged into `memory/<subdir>/behaviour.md` through `python/tools/behaviour_adjustment.py` and injected via `prompts/default/agent.system.behaviour.md`.
- Persistent agent data (memory fragments, solutions, scheduler state) sits under `memory/` and `tmp/scheduler`; mind their formats when writing migrations.

**Extensibility Tips**
- Extensions typically offload heavy work to background tasks (`_10_organize_history.py` starts compression, `_90_organize_history_wait.py` only syncs when over limits); follow that pattern for expensive hooks.
- Adding a tool or instrument requires both code and prompt metadata: implement the Python class, add an instruction under `prompts/default/agent.system.tool.<name>.md`, and document invocation examples.
- Instruments live in `instruments/custom/<name>` with an `.md` interface plus executable script—ideal for procedures that would bloat the system prompt.
- There is no automated test suite; sanity-check changes by launching the UI and calling `/health`, and use `python update_reqs.py` if dependency versions must be synchronized.
