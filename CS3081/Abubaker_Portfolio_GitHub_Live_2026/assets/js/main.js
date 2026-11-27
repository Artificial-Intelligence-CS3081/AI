const data=window.PORTFOLIO;
const featured=document.getElementById('featured-grid');
const grid=document.getElementById('project-grid');
const courseGrid=document.getElementById('courses-grid');
const renderCard=(p,wide=false)=>`<article class="project-card ${wide?'project-featured':''}" data-category="${p.categoryKey}"><a class="project-cover" href="project.html?id=${encodeURIComponent(p.slug)}" aria-label="Read about ${p.title}"><img src="${p.image}" alt="${p.imageAlt}" loading="lazy"><span class="project-cover-label">INTERFACE PREVIEW · ${p.year}</span></a><div class="project-meta"><span>${p.category}</span><span>${p.year}</span></div><div class="project-title-row"><h3><a href="project.html?id=${encodeURIComponent(p.slug)}">${p.title}</a></h3><a class="round-arrow" href="project.html?id=${encodeURIComponent(p.slug)}" aria-label="Open ${p.title} case study">↗</a></div><p class="project-desc">${p.short}</p><div class="project-tags">${p.tags.slice(0,4).map(t=>`<span>${t}</span>`).join('')}</div></article>`;
featured.innerHTML=data.projects.slice(0,2).map(p=>renderCard(p,true)).join('');
const archive=data.projects.slice(2);
function setFilter(filter){
 grid.innerHTML=archive.filter(p=>filter==='all'||p.categoryKey===filter).map(p=>renderCard(p)).join('');
 const buttons=document.querySelectorAll('.filter'); buttons.forEach(b=>{const active=b.dataset.filter===filter;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
}
document.querySelectorAll('.filter').forEach(b=>b.addEventListener('click',()=>setFilter(b.dataset.filter)));
setFilter('all');
// Credential cards use the actual images and verification links provided by Abubaker.
const certs=window.PORTFOLIO_CREDENTIALS.coursera;
const volunteerCertificates=window.PORTFOLIO_CREDENTIALS.volunteering;
let activeCredentialFilter='all',showAllCertificates=false;
const escapeHTML=(s)=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function renderCredentials(){
  const matched=certs.filter(c=>activeCredentialFilter==='all'||(activeCredentialFilter==='other'?!['Technical','Business','Design','Communication'].includes(c.category):c.category===activeCredentialFilter));
  const visible=showAllCertificates?matched:matched.slice(0,8);
  courseGrid.innerHTML=visible.map((c,i)=>`<article class="credential-card"><button type="button" class="certificate-preview" data-cert-image="${escapeHTML(c.image)}" data-cert-title="${escapeHTML(c.title)}" aria-label="Enlarge ${escapeHTML(c.title)} certificate"><img src="${escapeHTML(c.image)}" alt="Original Coursera certificate for ${escapeHTML(c.title)}" loading="lazy"><span class="preview-magnify" aria-hidden="true">↗</span></button><div class="credential-info"><div class="credential-category">COURSERA · ${escapeHTML(c.date)} </div><h3>${escapeHTML(c.title)}</h3><p>${escapeHTML(c.institution)}</p><a href="${escapeHTML(c.verify)}" target="_blank" rel="noopener noreferrer" aria-label="Verify ${escapeHTML(c.title)} on Coursera">Verify credential ↗</a></div></article>`).join('');
  const b=document.getElementById('show-all-credentials');
  b.hidden=matched.length<=8;
  b.setAttribute('aria-expanded',String(showAllCertificates));
  b.innerHTML=showAllCertificates?'Show fewer certificates <span aria-hidden="true">↑</span>':`Show all ${matched.length} certificates <span aria-hidden="true">↓</span>`;
  document.querySelectorAll('.credential-filter').forEach(x=>{const on=x.dataset.credentialFilter===activeCredentialFilter;x.classList.toggle('active',on);x.setAttribute('aria-pressed',String(on));});
}
renderCredentials();
document.querySelectorAll('.credential-filter').forEach(b=>b.addEventListener('click',()=>{activeCredentialFilter=b.dataset.credentialFilter;showAllCertificates=false;renderCredentials()}));
document.getElementById('show-all-credentials').addEventListener('click',()=>{showAllCertificates=!showAllCertificates;renderCredentials()});
const volunteerGrid=document.getElementById('volunteer-grid');
volunteerGrid.innerHTML=volunteerCertificates.map((v,i)=>`<article class="volunteer-card"><button type="button" class="volunteer-image certificate-preview" data-cert-image="${escapeHTML(v.image)}" data-cert-title="${escapeHTML(v.title)}" aria-label="Enlarge volunteering certificate ${escapeHTML(v.title)}"><img src="${escapeHTML(v.image)}" alt="Volunteering certificate preview with personal ID and verification QR hidden" loading="lazy"><span class="preview-magnify" aria-hidden="true">↗</span></button><div class="volunteer-info"><div class="volunteer-date">VOLUNTEERING / ${escapeHTML(v.date)}</div><h3>${escapeHTML(v.title)}</h3><p>${escapeHTML(v.organization)}</p><b>${v.hours} volunteer hours</b></div></article>`).join('');
const modal=document.getElementById('certificate-modal');
document.addEventListener('click',e=>{const btn=e.target.closest('[data-cert-image]');if(!btn)return;const img=document.getElementById('modal-certificate-image');img.src=btn.dataset.certImage;img.alt=btn.dataset.certTitle;document.getElementById('modal-certificate-caption').textContent=btn.dataset.certTitle;modal.showModal()});
modal.querySelector('.modal-close').addEventListener('click',()=>modal.close());
modal.addEventListener('click',e=>{if(e.target===modal)modal.close()});
document.getElementById('year').textContent=new Date().getFullYear();
const menu=document.getElementById('menu-toggle'),nav=document.getElementById('primary-nav');
menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false')}));
const observer=('IntersectionObserver' in window)?new IntersectionObserver(entries=>{for(const e of entries){if(e.isIntersecting){e.target.classList.add('in');observer.unobserve(e.target)}}},{threshold:.08}):null;
document.querySelectorAll('.reveal').forEach(x=>observer?observer.observe(x):x.classList.add('in'));
