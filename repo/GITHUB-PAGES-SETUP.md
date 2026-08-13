# GitHub Pages Setup — Phase 1a

This repo is now fully configured to serve as a real, SEO-crawlable Jekyll site directly from GitHub Pages,
with zero external hosting needed. Three things left, all in GitHub's web UI (can't be done from a repo push):

## 1. Fill in the two placeholders in `docs/_config.yml`

Open `docs/_config.yml` and replace:
- `YOUR-GITHUB-USERNAME` → your actual GitHub username or org name
- `YOUR-REPO-NAME` → this repo's name

These drive the `url`/`baseurl` Jekyll uses to build correct absolute URLs (sitemap, canonical tags, Open
Graph) before you have a custom domain.

## 2. Enable Pages

In the repo on GitHub: **Settings → Pages → Build and deployment → Source: "Deploy from a branch" → Branch:
`main`, folder: `/docs` → Save.**

GitHub will build the site (typically takes 1–2 minutes) and give you a live URL:
`https://YOUR-GITHUB-USERNAME.github.io/YOUR-REPO-NAME/`

## 3. Verify the build actually succeeded

Check the **Actions** tab in the repo — a "pages build and deployment" workflow run should show a green
checkmark. If it's red, click into it; the most common first-time failure is a YAML syntax issue in
`docs/_config.yml` (usually from step 1 not being done, or a stray character). Everything else in this repo
has already been validated locally (all 134 generated pages' front matter parsed successfully, all 183 SVGs
render correctly) — so if the build fails, it's almost certainly in `_config.yml` or a manual edit made after
this point.

## What you get once this is live

- Every one of the 60 Quick Reference use cases, all 60 Deep 8-Layer views, all 8 pattern docs, both
  architecture reference docs, and the 3 domain indices — **134 pages total** — each with its own real URL,
  page title, and meta description that search engines can actually index.
- An auto-generated `/sitemap.xml` (via the `jekyll-sitemap` plugin — nothing to maintain by hand; it
  regenerates every time GitHub rebuilds the site).
- A `/robots.txt` pointing at that sitemap.
- Open Graph / Twitter Card tags on every page (via `jekyll-seo-tag`), so links shared on LinkedIn/Slack/X
  show a real title and description instead of a bare URL.
- The interactive browsing app (same one as before) still lives at the site root `/` — nothing about that
  experience changed, it's just now sitting inside a real, crawlable site instead of being the entire site.

## When you buy your domain later

1. Add a file `docs/CNAME` containing just the domain, e.g.: `agenticworks.ai`
2. In `docs/_config.yml`, change `url:` to `https://agenticworks.ai` and delete the `baseurl:` line entirely
   (a custom domain doesn't sit under a repo-name subpath the way github.io does)
3. Point your domain's DNS at GitHub Pages per
   [GitHub's custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
4. In repo Settings → Pages, GitHub will detect the CNAME file and prompt you to enforce HTTPS — turn that on

## Known follow-ups (not blocking, but worth knowing about)

- The `og-image.png` referenced in the interactive app's meta tags doesn't exist yet — social link previews
  will just show no image until Phase 1c (visual polish) creates a real 1200×630 image.
- The interactive app's "Full markdown source" links (in the use-case detail panel) point to raw repo paths
  and will need updating to point at either the new Jekyll pages or GitHub's file browser once you've
  confirmed which you want them to do — flagged here so it doesn't get lost, not fixed yet.
