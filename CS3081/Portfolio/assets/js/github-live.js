/* Public GitHub activity. Runs entirely in the browser; no credentials required.
   New public repositories and pushed_at dates update automatically without rebuilding this portfolio.
   GitHub's Events API is eventually consistent and unauthenticated requests are rate-limited.
 */
(() => {
  'use strict';
  const USER = 'a30369814-code';
  const ROOT = `https://api.github.com/users/${USER}`;
  const status = document.getElementById('github-sync-status');
  const eventList = document.getElementById('github-events');
  const repoList = document.getElementById('github-repos');
  const repoHeader=document.getElementById('github-repos-heading');
  const refresh = document.getElementById('github-refresh');
  if (!status || !eventList || !repoList || !refresh) return;
  const knownRepos = window.PORTFOLIO.projects.filter(p => p.repo).map(p => ({
    name: new URL(p.repo).pathname.split('/').pop(),
    full_name: `${USER}/${new URL(p.repo).pathname.split('/').pop()}`,
    html_url: p.repo,
    language: p.tags[0], description: p.short,
    pushed_at: null
  }));
  let fetching = false, lastRequestAt = 0;
  const node = (name, cls, value) => {
    const el = document.createElement(name);
    if (cls) el.className = cls;
    if (value !== undefined) el.textContent = value;
    return el;
  };
  function safeURL(repo) {
    const path = typeof repo?.full_name === 'string' ? repo.full_name : '';
    return /^[\w.-]+\/[\w.-]+$/.test(path) ? `https://github.com/${path}` : `https://github.com/${USER}`;
  }
  function relative(date) {
    if (!date) return 'Recent repository';
    const time = new Date(date).getTime();
    if (!Number.isFinite(time)) return 'Recent';
    const min = Math.max(0, Math.floor((Date.now()-time)/60000));
    if (min < 1) return 'just now';
    if (min < 60) return `${min}m ago`;
    if (min < 1440) return `${Math.floor(min/60)}h ago`;
    if (min < 43200) return `${Math.floor(min/1440)}d ago`;
    return new Date(time).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});
  }
  function timeElement(date) {
    const el=node('time','event-time',relative(date));
    if(date) el.dateTime=date;
    if(date) el.title=new Date(date).toLocaleString('en-US');
    return el;
  }
  function renderRepos(data, live) {
    repoList.replaceChildren();
    if(repoHeader)repoHeader.firstChild.textContent=live?'RECENTLY UPDATED REPOSITORIES ':'KNOWN PUBLIC REPOSITORIES ';
    const publicRepos = data
      .filter(r=>r && !r.fork && !r.private)
      .filter(r=> !['a30369814-code','Abubaker_Portfolio_2026'].includes(r.name))
      .sort((a,b)=>(new Date(b.pushed_at||0).getTime())-(new Date(a.pushed_at||0).getTime()))
      .slice(0,7);
    publicRepos.forEach(r=>{
      const anchor=node('a','live-repo');anchor.href=safeURL(r);anchor.target='_blank';anchor.rel='noopener noreferrer';
      const left=node('span','repo-text');left.append(node('b',null,r.name||'Repository'),node('small',null,r.description||r.language||'View public source on GitHub'));
      const right=node('span','repo-right');right.append(timeElement(r.pushed_at),node('span','repo-open','↗'));
      anchor.append(left,right);repoList.append(anchor);
    });
    if (!publicRepos.length) repoList.append(node('p','empty-feed','No public repositories were returned.'));
    if(live) {
      document.querySelectorAll('.project-card').forEach(card => {
        const link=card.querySelector('a.project-cover')?.href||'';
        const slug=new URL(link,location.href).searchParams.get('id');
        const project=window.PORTFOLIO.projects.find(p=>p.slug===slug);
        if(!project?.repo)return;
        const repoName=new URL(project.repo).pathname.split('/').pop();
        const current=data.find(r=>r.name===repoName);
        if(!current || !current.pushed_at)return;
        let bottom=card.querySelector('.project-git-update');
        if(!bottom){bottom=node('div','project-git-update');card.append(bottom)}
        bottom.replaceChildren(node('span','update-dot','●'),node('span',null,` GitHub updated ${relative(current.pushed_at)}`));
      });
    }
  }
  function eventLabel(event) {
    const act = event.payload?.action;
    switch(event.type) {
      case 'PushEvent': return ['Code pushed',event.payload?.commits?.[0]?.message || 'New changes uploaded'];
      case 'CreateEvent': return ['New repository or branch', event.payload?.ref_type === 'repository' ? 'Repository created' : (event.payload?.ref || 'New branch')];
      case 'PullRequestEvent': return ['Pull request '+(act||'updated'), event.payload?.pull_request?.title || 'Reviewed changes'];
      case 'IssuesEvent': return ['Issue '+(act||'updated'), event.payload?.issue?.title || 'Project issue'];
      case 'ReleaseEvent': return ['New release',event.payload?.release?.name||'Published release'];
      case 'WatchEvent': return ['Starred a repository','GitHub activity'];
      case 'ForkEvent': return ['Forked a repository','GitHub activity'];
      case 'PublicEvent': return ['Repository made public','GitHub activity'];
      default: return null;
    }
  }
  function renderEvents(events, recentRepos=[]) {
    eventList.replaceChildren();
    const usable = Array.isArray(events) ? events.filter(e=>eventLabel(e) && e.repo?.name && e.public!==false).slice(0,7) : [];
    if(usable.length){
      usable.forEach(e=>{
        const content=eventLabel(e), item=node('li','activity-item');
        const mark=node('span','event-mark',e.type==='PushEvent'?'↑':'↗');
        const info=node('div','event-content'),title=node('strong',null,content[0]),details=node('span',null,content[1]);
        const link=node('a',null,String(e.repo.name).split('/').pop());link.href=safeURL({full_name:e.repo.name});link.target='_blank';link.rel='noopener noreferrer';
        info.append(title,link,details);item.append(mark,info,timeElement(e.created_at));eventList.append(item);
      });
    }else if(recentRepos.length){
      // Repositories list is up to date even if the Events endpoint has no activity to show.
      recentRepos.slice().sort((a,b)=>new Date(b.pushed_at||0)-new Date(a.pushed_at||0)).slice(0,5).forEach(r=>{
        const item=node('li','activity-item'),mark=node('span','event-mark','↑'),info=node('div','event-content'),title=node('strong',null,'Repository updated');
        const link=node('a',null,r.name);link.href=safeURL(r);link.target='_blank';link.rel='noopener noreferrer';
        info.append(title,link,node('span',null,'Most recent repository push'));item.append(mark,info,timeElement(r.pushed_at));eventList.append(item);
      });
    } else {
      eventList.append(node('li','empty-feed','No recent public activity is available. Visit GitHub for full history.'));
    }
  }
  async function getJSON(path) {
    const response=await fetch(`${ROOT}/${path}`,{
      method:'GET',headers:{Accept:'application/vnd.github+json'},cache:'no-store'
    });
    if (!response.ok) throw Error(`GitHub API ${response.status}`);
    return response.json();
  }
  async function loadGithub(){
    if(fetching || Date.now()-lastRequestAt<15000)return;
    fetching=true;lastRequestAt=Date.now();refresh.disabled=true;status.textContent='Connecting to GitHub…';
    const results=await Promise.allSettled([
      getJSON('repos?per_page=100&sort=pushed&direction=desc'),
      getJSON('events/public?per_page=30')
    ]);
    const repos = results[0].status==='fulfilled' && Array.isArray(results[0].value) ? results[0].value:null;
    const events = results[1].status==='fulfilled' && Array.isArray(results[1].value) ? results[1].value:null;
    if(repos){renderRepos(repos,true)}else renderRepos(knownRepos,false);
    if(events || repos)renderEvents(events,repos||[]);
    else {eventList.replaceChildren(node('li','empty-feed','Live activity could not be loaded right now. Check the GitHub profile for recent updates.'));}
    if(repos && events){status.textContent='Live · checked '+new Date().toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'});}
    else if(repos){status.textContent='Repositories live · activity feed unavailable';}
    else if(events){status.textContent='Activity live · repository list unavailable';}
    else{status.textContent='Live GitHub temporarily unavailable · showing known projects';}
    status.title='Public GitHub events may take several minutes to appear.';
    fetching=false;refresh.disabled=false;
  }
  refresh.addEventListener('click',loadGithub);
  renderRepos(knownRepos,false);
  eventList.replaceChildren(node('li','activity-loading','Loading latest public GitHub events…'));
  loadGithub();
  setInterval(()=>{if(document.visibilityState==='visible')loadGithub()},5*60*1000);
})();
