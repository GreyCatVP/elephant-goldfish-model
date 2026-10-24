# egm.dev

The Elephant-Goldfish Model website at [egm.dev](https://egm.dev), hosted on GitHub Pages.

| Light | Dark |
| --- | --- |
| ![Hero, light scheme](screenshots/hero-light.png) | ![Hero, dark scheme](screenshots/hero-dark.png) |

<details>
<summary>Full page and mobile</summary>

![Full page, light scheme](screenshots/full-light.png)

![Mobile, 375px wide](screenshots/mobile.png)

</details>

## Stack

- [Astro](https://astro.build) for the static site.
- [Material Web](https://github.com/material-components/material-web) for styles.
- [Google Sans Flex](https://fonts.google.com/specimen/Google+Sans+Flex) and
  [Google Sans Code](https://fonts.google.com/specimen/Google+Sans+Code), self-hosted under
  [src/assets/fonts/](src/assets/fonts/) (OFL).

## Rules

- No analytics, cookies, third-party scripts, or runtime requests to Google hosts.
- Theme only through Material Web [design tokens](src/styles/tokens.css) and the
  components' documented custom properties. Do not restyle component boxes.
- Keep skill names and commands identical to the [repository README](../README.md).

## Develop

Run from `site/` with Node.js 22.12 or newer:

```sh
npm ci
npm run dev      # http://localhost:4321
npm run check
npm run build    # output: dist/
npm run capture  # rebuild and refresh images
```

After visual changes, run `npm run capture`. It requires Chrome; set `CHROME_PATH`
if needed. Edit the [social-image template](scripts/og.html) to change the social image.

## Deploy

[Deploy site](../.github/workflows/deploy-site.yml) publishes changes to `site/`
on `main`. It also supports manual runs.
