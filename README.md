# Lune Support

The support website for **Lune – Private Period Tracker**, published by **Polaris Labs** (Canada):
https://polarislabsca.github.io/lune-support/

| Page | English | 繁體中文 | 简体中文 |
|---|---|---|---|
| Support | `/` | `/zh-hant/` | `/zh-hans/` |
| Privacy Policy (the App Store privacy URL) | `/privacy/` | `/zh-hant/privacy/` | `/zh-hans/privacy/` |
| Terms of Use (**draft** until the lawyer's review) | `/terms/` | `/zh-hant/terms/` | `/zh-hans/terms/` |
| Feedback (Tally form) | `/feedback/` | `/zh-hant/feedback/` | `/zh-hans/feedback/` |

The Lune app opens these paths in the system browser (`Lune/Logic/SupportSite.swift` in the app repository).
Don't rename or move them.

## Rules

- Static HTML and CSS only. The one script is `feedback-form.js`, loaded only by the three feedback pages,
  which embeds the Tally form.
- No analytics, no cookies, no external fonts, images or stylesheets. Every page carries a
  Content-Security-Policy and `no-referrer`.
- The feedback pages ask people not to include health details; the privacy policy names Tally.
- Legal text changes go to all three languages, and the Chinese pages say the English version applies.

## Feedback form

The Tally form ID lives in exactly one place: `LUNE_TALLY_FORM_ID` at the top of `feedback-form.js`. Until
it's set, every feedback page shows a "not available yet" note with the email address.

1. In Tally, create one form: a star rating, "Message" (long text; its help text:
   "Please don't include health details."), "Email (optional, only if you'd like a reply)", and a
   **hidden field** named `language` (the pages fill in `en`, `zh-Hant` or `zh-Hans`). Labels can be in
   English and Chinese, for example "Message / 訊息 / 消息". Turn off Tally's own analytics and any
   third-party integrations.
2. Publish it and copy the ID at the end of its share link (`https://tally.so/r/<ID>`).
3. Set `var LUNE_TALLY_FORM_ID = "<ID>";` in `feedback-form.js`, run `tools/check.sh`, commit and push.
4. Open each feedback page in Safari (and one in Chrome) and send a test message.

## Checking locally

```sh
tools/check.sh
```

It checks every page's structure, links and language links, that nothing loads from another site (except
Tally on the feedback pages), that the HTML is well-formed, and that each page is served with 200 by a local
server. Preview with `python3 -m http.server 8765` and open http://127.0.0.1:8765/.

## Publishing

GitHub Pages, from the `main` branch, root folder (`.nojekyll` serves the files as they are).

Contact: [polarislabs.ca@gmail.com](mailto:polarislabs.ca@gmail.com)
