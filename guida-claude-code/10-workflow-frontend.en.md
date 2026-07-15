# 10 - The frontend workflow: Claude with a real browser

> Verified on July 15, 2026. This is THE chapter for frontend developers:
> here the verification loop (ch. 11) becomes visual.

## The quality leap

Without a browser, Claude writes CSS blind: it makes a change, you look,
you describe in words what's wrong ("no, the padding is still too tight"),
it tries again. You are its visual system, and you're the bottleneck.
With a browser connected, **Claude sees what you see**: it navigates the
page, reads the console, takes screenshots, compares against the design
and corrects itself. The loop closes. You step out of the back-and-forth
and step back in only to give final approval.

There are two ways to connect a browser, plus a third route for
debugging. Let's go through them with the same structure: what it is,
how to install it, how it works.

## Route 1: Playwright MCP (free, open source)

**What it is**: an MCP server (ch. 08) that gives Claude a browser of its
own, headless or visible, to drive: opening pages, clicking, filling out
forms, taking screenshots, reading the console.

**How to install it**: one line, using the syntax from ch. 08 (server
name, `--`, launch command):

```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

> **Tested live on Jul 15, 2026**, two real traps encountered:
> 1. by default the server looks for **Google Chrome**: if you don't have
>    it (or prefer something else), pick the engine with `--browser firefox`
>    or `--browser chromium` at the end of the command;
> 2. on first launch it may ask for a browser you don't have cached; this
>    is fixed with `npx @playwright/mcp install-browser [firefox]`.
> Once that's done, ask it to "open example.com and tell me the title and
> h1" and you get the right answer from a real browser (verified here on
> Firefox: the user agent did report Gecko/Firefox).

**How it works**: from here on, whenever you ask for something involving a
page, Claude uses the server's tools to drive the browser. The technical
detail that makes it powerful: it doesn't reason (only) over pixels, but
over the **accessibility tree**, the structured representation of the page
that the browser builds for screen readers. This is deterministic data
("there's a button labeled 'Save'", "this field is required"), which
Claude reads precisely where a screenshot would leave ambiguity. Perfect
for verifying flows, filling out forms, and reading console errors. It
also doubles as the foundation for e2e tests. A bonus that isn't small:
if your UI is unreadable to the accessibility tree, you've just found an
a11y problem, the same one a screen reader would have.

## Route 2: the official Chrome extension (Anthropic, for subscribers)

**What it is**: Claude inside *your* Chrome, not in a separate browser.
The practical difference: your already-authenticated sessions, your
actual state, nothing to log back into or rebuild. And more focused
responses: Playwright on complex pages can return trees running to tens
of thousands of tokens, while the extension works more selectively.

**How to get it**: it's tied to your subscription; check availability for
your plan on claude.ai. If you have it, it's the most convenient route for
day-to-day interactive development; Playwright remains the workhorse for
automation and for anyone starting from scratch.

## The third route: Chrome DevTools MCP

For deep debugging there's a third server:

```bash
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

It speaks Chrome's DevTools protocol: network, performance, coverage, the
tabs you'd open yourself in DevTools, read by Claude. It complements
Playwright: one drives the page, the other listens to its vitals.

## The screenshot-driven cycle

With the browser connected, the official pattern for implementing from a
design becomes available. Three moves:

1. **Provide the mock**: paste the design screenshot (`Ctrl+V` in the
   session) or connect Figma (below). This is the *target*: an image, not
   a verbal description.
2. **Ask for the full loop**, not just the implementation: "implement this
   component; then start the dev server, open the page, take a screenshot,
   compare it against the mock, list the differences and fix them. Repeat
   until they match." The key phrase is *repeat until*: that's what turns
   a single attempt into a cycle.
3. Claude iterates on its own: implement → look (a real screenshot, from a
   real browser) → compare → fix → look again.

What to expect: the first iteration will be at 70%; the third, nearly
indistinguishable from the mock. Your job shifts from "describing the
differences in words" to "approving the result", which is exactly the
work you want to be doing.

The same loop works in reverse, for visual bugs: paste the screenshot of
the glitch and ask "reproduce it, find the cause, fix it, prove it with an
after screenshot". The final screenshot is the evidence that the fix works.

## Figma

**What it is**: Figma's official MCP server, which connects the design
system to the session. It's a remote server (HTTP, ch. 08): no local
processes; you add it with the URL and authenticate with your Figma
account:

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

**How it works**: Claude reads frames, components and design tokens
straight from the Figma file, not from a screenshot but from the data.
"Use the design system's spacing tokens, not hand-picked values" stops
being wishful thinking: Claude actually sees the tokens. And since 2026
the Claude Code integration is bidirectional, code → canvas too.

## The full picture

With this stack (Playwright or the extension + Figma + the tests from
ch. 11), a frontend task sounds like this:

> "Implement the product card from the Figma frame 'ProductCard v2'.
> Component in `src/components/`, CSS modules, mock data. Then: dev
> server, screenshots at the 375px and 1280px viewports, compare against
> the frame, fix the differences. Close out when the screenshots match and
> `npm run test` passes."

Note the three roles: the design as **verifiable input** (the Figma frame,
not a description), the browser as the **verification tool** (the
screenshots at the two viewports), the tests as the **gate** (nothing
closes until they pass). It's chapter 11 applied to the frontend, and it's
why this setup pays back the hour it costs to set up.

---

**In short**: Playwright MCP right away (one line, free), the Chrome
extension if your plan includes it, Figma when you work from designs. And
starting tomorrow, no more "fix the padding" in words: screenshot, loop,
evidence.
