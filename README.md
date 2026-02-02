# QuickNote
Capture only what you choose with Vision-Language (VL) models.

[中文介绍](./README_zh.md)

## Introduction
QuickNote is a lightweight, privacy-minded capture workflow for iOS and macOS.

Instead of continuously recording everything on your screen, QuickNote uses an intentional model: you only capture what matters. When you take a screenshot, QuickNote sends the image (plus your prompt) to a Vision-Language model, converts the result into clean Markdown, and saves it to [Memos](https://github.com/usememos/memos) for long-term search and organization.

The core idea is simple:
- Screenshots are easy to take, but hard to search later.
- LLM-structured notes are easy to search, tag, and reuse.
- You should control what gets saved.

QuickNote was inspired by the discussion around Microsoft [Recall](https://en.wikipedia.org/wiki/Windows_Recall), but follows the opposite design philosophy: selective memory over passive, always-on recording.

## How It Works
```text
Screenshot + prompt
      -> Vision-Language model
      -> Parsed Markdown
      -> Memos
```

## What QuickNote Solves
- Turn raw screenshots into searchable notes.
- Keep both the original image and extracted text context.
- Make capture frictionless on mobile and desktop.
- Organize notes in Memos with keywords and hashtags.

## Current Setup
QuickNote is currently built around [Memos](https://github.com/usememos/memos) as the note interface and storage layer.

On the client side:
- **iOS**: Trigger capture with Apple Shortcuts.
- **macOS**: Trigger the same Shortcut via hotkey (for example through Raycast).

## iOS Shortcut
Use this shortcut template:

[QuickNote iOS Shortcut](https://www.icloud.com/shortcuts/66484a23c6094afbb6c2078c5cd237d9)

After importing it, update the request URL so screenshots are sent to your own QuickNote server.

## macOS Trigger (Suggested)
On macOS, you can bind the Shortcut to a global hotkey with Raycast.

Example:
- Hotkey: `Command + F2`
- Priority: set to high (so the hotkey is reliably captured)

## Live Demo
### iPhone
<video src="./assets/live_demo.mp4" controls="controls" width="100%" height="auto">
</video>

### macOS
<video src="./assets/live_demo_mac.mp4" controls="controls" width="100%" height="auto">
</video>

## Quick Start
QuickNote depends on Memos. Users can deploy Memos first independently, then configure and run the QuickNote server. Or to make a quick setup, users can also use below docker compose. 
```bash
cd server
cp .env.example .env
# edit .env and set your provider + API keys + memos settings
docker compose up
```

Once the server is running, point your Shortcut to the server URL and start capturing.
