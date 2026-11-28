/* Show the current latest commit from GitHub on this project's case study.
   This updates on every page visit, even when the site's authored case-study text hasn't changed.
 */
(() => {
  const box = document.getElementById('case-live');
  const text = document.getElementById('case-live-text');
  const link = document.getElementById('case-live-link');
  if (!box || !text || !link || !p.repo) {if(box)box.hidden=true;return;}
  const m = p.repo.match(/^https:\/\/github\.com\/([\w.-]+)\/([\w.-]+)\/?$/);
  if (!m) {box.hidden=true;return;}
  const [owner,repo] = [m[1],m[2]];
  (async () => {
    try {
      const res = await fetch(`https://api.github.com/repos/${owner}/${repo}/commits?per_page=1`,{
        headers:{Accept:'application/vnd.github+json'},cache:'no-store'
      });
      if(!res.ok)throw Error(String(res.status));
      const items=await res.json();
      const commit=items?.[0];
      if(!commit?.commit?.message)throw Error('No commits');
      const timestamp=commit.commit.author?.date || commit.commit.committer?.date || null;
      const msg=String(commit.commit.message).split('\n')[0].slice(0,160);
      text.textContent=timestamp ? `${msg} · ${new Date(timestamp).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}` : msg;
      if(typeof commit.html_url==='string' && commit.html_url.startsWith(`https://github.com/${owner}/${repo}/commit/`)){
        link.href=commit.html_url;link.hidden=false;
      }
    } catch {
      text.textContent='Live commit details are temporarily unavailable. The repository link above remains available.';
    }
  })();
})();
