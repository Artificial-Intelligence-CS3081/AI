# Abubaker Baobaid — Portfolio with Live GitHub, Coursera & Volunteering

A static, responsive HTML/CSS/JavaScript portfolio based on Abubaker's previous editorial portfolio. Updated using the original **15 Coursera PDFs** and **5 volunteering certificates** provided on 26 November 2026. No copyrighted template/code/assets were copied from the example portfolio; this is Abubaker's own design and content.

## View locally

1. Unzip the package.
2. Open `index.html` in Chrome, Safari, or Firefox. Internet access is needed for the **public GitHub** live feed and optional Google Fonts.
3. Click **GitHub Live**, **Certificates**, or **Volunteering** in the navigation.
4. Use **View CV** or **Download CV**; both the updated one-page designed PDF and an editable DOCX are in `assets/`.

No build step, login, GitHub token, or paid service is needed.

## Live GitHub integration

`assets/js/github-live.js` uses the official public GitHub REST API (no credentials) to read:

- `https://api.github.com/users/a30369814-code/events/public?per_page=30` — latest public activity, including pushes and new repositories.
- `https://api.github.com/users/a30369814-code/repos?per_page=100&sort=pushed&direction=desc` — public repositories ordered by their most recent push.

When the page opens, it fetches both endpoints. It automatically refreshes **every 5 minutes while the page is visible**; visitors can also click **Refresh**. The *Recently Updated Repositories* list includes newly public repositories and shows their real latest push dates. Featured project cards also get their latest GitHub update time. In each case study, `assets/js/project-live.js` fetches the newest commit and displays its actual commit message/date/link when available.

**What refreshes automatically:** public activity, recent repository list, new public repositories, featured projects' GitHub update labels, and case-study latest commit information (when opened).

**What remains manually authored:** project summaries, detailed case-study narrative, project preview images, downloadable CV, awards and static content. These require a site change/redeployment if edited. Only *public* GitHub information can appear automatically. The GitHub Events API may be delayed, and unauthenticated requests have rate limits. If GitHub is temporarily unavailable, the site clearly shows known project links rather than inventing live activity. It never caches a token or asks for your password.

## Coursera credentials — 15 verified items

- The images under `assets/certificates/coursera/` are renders of the original certificates in `Coursera.zip`.
- Every verification URL in `assets/js/credentials.js` was extracted from its PDF and checked against the certificate ID.
- Visitors can filter certificates, enlarge each image and open the official **Verify credential** Coursera page.
- The site includes all **15**, and initially shows eight for a cleaner layout.

### Volunteering — 5 certificates, 110 total documented hours

- Five scanned volunteering certificates were reviewed visually from `التطوع.zip`.
- The **published images** under `assets/certificates/volunteering/` are privacy-safe copies: government identity numbers and QR verification codes were permanently covered on the rasterized images before they were saved.
- **Do not upload the original volunteering PDFs publicly** without checking their personally identifying fields. Those PDFs are **not included** in this package.
- Activity labels summarize the certificate descriptions in English; the displayed hours are the documented values: **20 + 60 + 15 + 10 + 5 = 110 hours**.

## CV

- `cv.html` — editable website CV layout, with linked selected Coursera certificates and volunteering summary.
- `assets/Abubaker_Baobaid_CV.pdf` — designed 1-page A4 PDF with links.
- `assets/Abubaker_Baobaid_CV_Editable.docx` — 1-page, ATS-friendly Word CV.

## Publishing to GitHub Pages

Create a public repository named **`a30369814-code.github.io`** in your own GitHub account, then upload **the contents of this folder** (not the enclosing folder) to its `main` branch. In the repository go to **Settings → Pages → Build and deployment → Deploy from a branch → main / (root)**. The site will be at:

**https://a30369814-code.github.io/**

Once it is published, the GitHub feed will retrieve fresh public information when visitors open the page. **This bundle has not been published or pushed to your account.**

## Editability and design notes

- `assets/js/data.js`: featured projects, contact details and case-study descriptions.
- `assets/js/credentials.js`: certificates, images, dates, verification links, volunteering entries.
- `assets/js/main.js`: cards, filtering, certificate popup and navigation.
- `assets/js/github-live.js`: live public GitHub feed and recent repositories.
- `assets/js/project-live.js`: latest GitHub commit for project details.
- `assets/css/style.css`: site styling and responsive breakpoints.

The original selected project images remain **source-informed illustrations/reconstructions**, not verified running-app screenshots. They can be replaced with genuine screenshots later. The Dean's List picture was supplied by Abubaker.
