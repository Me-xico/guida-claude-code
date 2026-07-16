# 12 - Prompt engineering for Claude Code

> Source: official best practices and established community patterns,
> July 2026.

## The right mental model

The starting problem is almost always the same: you treat Claude Code like
a search engine to pry answers out of, terse question, terse answer,
disappointment. The mental model that works is different: it's a **bright
junior you manage**. A junior whose memory is wiped at every session
(that's why CLAUDE.md exists), extremely fast, never offended, but who,
given a vague request, produces a vague result, exactly like a real junior
handed a ticket that just says "fix the login".

You're the PM: the clearer the brief, the better the delivery. This entire
chapter is that sentence, unpacked.

## Specificity: success criteria, not adjectives

The pain: you ask "improve this component", you get a refactor that
touches twenty unrelated lines, and the real problem, the re-renders, is
still there. It's not the model's fault: "improve" doesn't say *what* has
to be true at the end.

Weak: "improve this component".
Strong:

> "Reduce `ProductList` re-renders: memoize the callbacks passed to
> children, move the filter into a `useMemo`, and verify with the Profiler
> that when `query` changes only the list re-renders. Don't change the
> public API."

The difference isn't length: it's that the second one has **verifiable
criteria** (ch. 11, "verify with the Profiler that…") and **constraints**
(what not to touch, "don't change the public API"). Adjectives like
"better", "clean", "modern" aren't instructions: they're hopes. The quick
test for your prompt: *could a colleague who doesn't know the context tell
whether the job was done well?* If not, the criteria are missing.

*The signal to watch for*: the result is "technically what I asked for"
but not what you wanted. The problem was in the brief.

## Context and constraints, not micro-instructions

The opposite mistake to vagueness: dictating *how* to do every step, line
by line. There's no need: that's what the model is for; it knows how to
write code. What you need to provide instead is what the model **cannot
know** by looking at the repo:

- the *why*: "this form is the payment funnel: the priority is not
  breaking the tracking", which changes every downstream decision
- the **constraints**: "Node 18, no new dependencies"
- the **references**: "`@src/components/Form.tsx` is the pattern to
  follow"

And pass the context in the richest form available: reference files with
`@` (instead of describing them), paste errors **in full** (the stack
trace contains the answer more often than you'd think), attach screenshots
(`Ctrl+V`) when the problem is visual. A prompt that puts the pieces
together:

> "The funnel tracking broke after the latest refactor. This form is the
> payment funnel: top priority is not losing events. Console error:
> [pasted in full]. The correct event-sending pattern is in
> `@src/analytics/track.ts`. Constraint: no new dependencies."

Why it works: the model reasons over what's in its context. The why,
constraints and references are exactly the information it can't deduce on
its own: everything else it can.

## Decomposition: ask for the first step, not the journey

Asking for a whole feature in one prompt is the greed mistake, mistake 2
in ch. 13. Instead:

> "Let's build the cart in steps. Step 1: the data layer only — a
> `useCart` hook with add, remove, quantity, and the Vitest tests. No UI,
> no persistence for now. Then we meet back here and decide on step 2."

Each finished and verified step is a checkpoint (in the literal sense:
ch. 03) to build the next one on. If step 2 goes wrong, you return to
solid ground instead of untangling a mess.

For large features, the official pattern is **having Claude interview
you**, useful precisely because the requirements you *think* are clear
aren't:

> "I need to build X. Before writing code, interview me: ask the questions
> needed to clarify requirements and edge cases, then write a spec in
> SPEC.md."

Claude's questions surface edge cases you hadn't thought of (what happens
to the cart when the user logs out? do discounts stack?). Review the spec,
`/clear`, and in a fresh session: "implement SPEC.md, step 1". The spec
replaces a hundred mid-flight corrections, and the session that
implements it starts clean, without the noise of the discussion.

*The signal to watch for*: you're writing a prompt that contains "and
then… and also…". Stop at the first "and".

## Iterating: concrete feedback, not repetition

The pain: the result is wrong, you re-explain the same thing with more
emphasis ("no, the button has to go ON THE RIGHT"), and it goes wrong
again. Repeating yourself louder adds no information. Provide **new
material** instead: the exact error, the test output, the screenshot of
what's actually on screen. "It doesn't work" gives Claude nothing to work
with; a stack trace does:

> "The fix isn't enough: on submit I now get this — [full stack trace].
> Here's also a screenshot of the form's state [Ctrl+V]. Note that it
> only happens when the email field is empty."

And remember the 2-attempt rule (ch. 03): after the second failed round,
`/clear` and rephrase from scratch, folding in what you've learned. The
reason is mechanical: every failed correction stays in the context and
weighs on the responses that follow. Accumulated corrections pollute more
than they help. The third attempt in the same session starts at a
disadvantage; the same prompt, rewritten better in a clean session, starts
at an advantage.

## Before/after

| Weak | Strong |
|---|---|
| "fix the login bug" | "login fails with a 401 after the token refresh — here's the log: […]. The flow is in `@src/auth/`. Find the cause, propose the fix, and add a test that reproduces the case" |
| "add the tests" | "cover `useCart` with Vitest: add, remove, quantity at zero, empty cart. Look at `@src/hooks/useAuth.test.ts` for the style" |
| "redo the navbar css" | "the navbar should become sticky with blur on scroll, as in this screenshot [Ctrl+V]. CSS modules only, no libraries. Then a screenshot of the result" |

Note the pattern the strong versions share: an observable fact (log,
screenshot) + where to look (`@`) + a completion criterion (tests, a
screenshot of the result). It's always the same three ingredients.

---

**In short**: verifiable criteria + constraints + context, one step at a
time, feedback made of evidence. The perfect prompt doesn't exist; the
prompt with a verifiable success criterion does, and that's the one that
counts. The next chapter (17) takes this method one step before the
prompt: researching and designing before building.
