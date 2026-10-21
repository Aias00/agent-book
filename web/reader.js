/* Directory, font and reading progress enhancements; native links work without JS. */
(() => {
  'use strict';
  const root = document.documentElement;
  const read = key => { try { return localStorage.getItem('agent-book:' + key); } catch { return null; } };
  const save = (key, value) => { try { localStorage.setItem('agent-book:' + key, value); } catch { /* Optional persistence. */ } };
  const menu = document.getElementById('chapter-menu');
  const mobile = matchMedia('(max-width: 900px)');
  const setMenu = () => { menu.open = !mobile.matches; };
  setMenu();
  mobile.addEventListener('change', setMenu);
  const controls = document.querySelector('.enhanced-controls');
  controls.hidden = false;
  const smaller = document.getElementById('font-smaller');
  const larger = document.getElementById('font-larger');
  const saved = Number(read('font-size'));
  let size = saved >= 15 && saved <= 24 ? saved : mobile.matches ? 17 : 18;
  const applySize = () => {
    root.style.setProperty('--body-size', size + 'px');
    smaller.disabled = size <= 15;
    larger.disabled = size >= 24;
  };
  for (const [button, step] of [[smaller, -1], [larger, 1]]) button.addEventListener('click', () => {
    size = Math.max(15, Math.min(24, size + step));
    save('font-size', String(size));
    applySize();
  });
  applySize();
  const page = document.body.dataset.page;
  const links = [...document.querySelectorAll('#TOC a')];
  if (page !== 'index') save('last-page', page + '.html');
  else {
    const previous = read('last-page');
    const link = links.find(item => item.getAttribute('href') === previous);
    if (link) {
      const note = document.getElementById('resume-note');
      const resume = document.createElement('a');
      resume.href = previous;
      resume.textContent = '继续阅读：' + link.textContent;
      note.append(resume);
      note.hidden = false;
    }
  }
  const bar = document.getElementById('progress-bar');
  function progress() {
    const distance = document.documentElement.scrollHeight - innerHeight;
    bar.style.width = (distance > 0 ? Math.max(0, Math.min(100, scrollY / distance * 100)) : 0) + '%';
  }
  addEventListener('scroll', progress, { passive: true });
  addEventListener('resize', progress);
  progress();
})();

/* BEGIN AIAS SHARED READER */
/* Aias Reader 1.0. Shared preference across books on aias00.github.io. */
(() => {
  'use strict';
  const root = document.documentElement;
  const key = 'aias-reader-theme';
  const read = () => { try { return localStorage.getItem(key); } catch { return null; } };
  let theme = read() === 'dark' ? 'dark' : 'light';
  let control;
  function apply() {
    root.dataset.theme = theme;
    if (document.body) document.body.classList.toggle('dark', theme === 'dark');
    const palette = document.querySelector('[data-md-component="palette"]');
    if (palette) {
      const scheme = theme === 'dark' ? 'slate' : 'default';
      document.body.dataset.mdColorScheme = scheme;
      const selected = palette.querySelector(`input[data-md-color-scheme="${scheme}"]`);
      if (selected) {
        selected.checked = true;
        palette.querySelectorAll('label[for]').forEach(label => { label.hidden = label.htmlFor === selected.id; });
      }
    }
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#1c1f24' : '#f7f7f3');
    if (!control) return;
    if (control.tagName === 'SELECT') {
      control.value = theme;
    } else {
      control.textContent = theme === 'dark' ? '切换浅色' : '切换深色';
      control.setAttribute('aria-pressed', String(theme === 'dark'));
    }
    control.setAttribute('aria-label', theme === 'dark' ? '切换到浅色模式' : '切换到深色模式');
  }
  apply();
  function initialize() {
    const palette = document.querySelector('[data-md-component="palette"]');
    if (palette) {
      palette.addEventListener('change', event => {
        theme = event.target.dataset.mdColorScheme === 'slate' ? 'dark' : 'light';
        try { localStorage.setItem(key, theme); } catch { /* Optional persistence. */ }
        apply();
      });
      apply();
      return;
    }
    control = document.querySelector('#theme-toggle, #theme, select[name="theme"]');
    if (!control) {
      const bar = document.createElement('div');
      bar.className = 'aias-reader-tools';
      const home = document.createElement('a');
      home.href = 'https://aias00.github.io/#books';
      home.textContent = 'Aias · 电子书架';
      control = document.createElement('button');
      control.type = 'button';
      bar.append(home, control);
      (document.querySelector('main') || document.body).prepend(bar);
    }
    control.hidden = false;
    control.classList.add('aias-reader-theme');
    if (control.tagName === 'SELECT') {
      control.replaceChildren(...['light', 'dark'].map(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value === 'light' ? '浅色' : '深色';
        return option;
      }));
    }
    const eventName = control.tagName === 'SELECT' ? 'change' : 'click';
    // Capture before legacy handlers; all other reader controls keep working.
    document.addEventListener(eventName, event => {
      if (!control.contains(event.target)) return;
      event.stopImmediatePropagation();
      if (eventName === 'click') event.preventDefault();
      theme = control.tagName === 'SELECT' ? control.value : theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(key, theme); } catch { /* Reading works without storage. */ }
      apply();
    }, true);
    apply();
  }
  // Legacy initializers finish first; the shared preference is applied last.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(initialize, 0), { once: true });
  } else {
    setTimeout(initialize, 0);
  }
  addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    theme = event.newValue === 'dark' ? 'dark' : 'light';
    apply();
  });
})();
/* END AIAS SHARED READER */
