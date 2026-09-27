async (page) => {
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  const results = [];
  const url = 'http://127.0.0.1:8768/output/site/elearning/part-05/contract-negotiation-basics/';
  for (const width of [1920, 1440, 390]) {
    await page.setViewportSize({width, height: width === 1920 ? 1080 : 1200});
    await page.goto(url + '?qa=' + Date.now() + '-' + width);
    for (let n = 1; n <= 14; n += 1) {
      await page.locator('.slide-jump').nth(n - 1).click();
      const qa = await page.evaluate(() => {
        const issues = [], tolerance = 1.5;
        const slide = document.querySelector('.slide');
        const sr = slide.getBoundingClientRect();
        const boxes = Array.from(slide.querySelectorAll('th, td'));
        const textRuns = [];
        const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
        while (walker.nextNode()) {
          const node = walker.currentNode;
          if (!node.textContent.trim()) continue;
          const range = document.createRange();
          range.selectNodeContents(node);
          for (const rect of range.getClientRects()) {
            if (rect.width && rect.height) textRuns.push({node, rect});
          }
        }
        let minimumPadding = Infinity;
        for (const {node, rect} of textRuns) {
          if (rect.left < sr.left - tolerance || rect.right > sr.right + tolerance ||
              rect.top < sr.top - tolerance || rect.bottom > sr.bottom + tolerance) {
            issues.push('text outside slide: ' + node.textContent.trim().slice(0, 60));
          }
        }
        for (const box of boxes) {
          const br = box.getBoundingClientRect(), style = getComputedStyle(box);
          if (box.scrollWidth > box.clientWidth + tolerance || box.scrollHeight > box.clientHeight + tolerance) {
            issues.push('table cell overflow: ' + box.textContent.trim().slice(0, 60));
          }
          for (const {node, rect} of textRuns) {
            if (box.contains(node)) {
              minimumPadding = Math.min(minimumPadding, rect.left - br.left, br.right - rect.right,
                rect.top - br.top, br.bottom - rect.bottom);
              if (rect.left < br.left + parseFloat(style.paddingLeft) - tolerance ||
                  rect.right > br.right - parseFloat(style.paddingRight) + tolerance ||
                  rect.top < br.top + parseFloat(style.paddingTop) - tolerance ||
                  rect.bottom > br.bottom - parseFloat(style.paddingBottom) + tolerance) {
                issues.push('table text lacks padding: ' + node.textContent.trim().slice(0, 60));
              }
            } else if (Math.min(rect.right, br.right) - Math.max(rect.left, br.left) > tolerance &&
                       Math.min(rect.bottom, br.bottom) - Math.max(rect.top, br.top) > tolerance) {
              issues.push('table cell obscures external text: ' + node.textContent.trim().slice(0, 60));
            }
          }
        }
        for (let i = 0; i < boxes.length; i += 1) for (let j = i + 1; j < boxes.length; j += 1) {
          const a = boxes[i].getBoundingClientRect(), b = boxes[j].getBoundingClientRect();
          if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > tolerance &&
              Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > tolerance) issues.push('unrelated table cells overlap');
        }
        if (slide.scrollWidth > slide.clientWidth + tolerance || slide.scrollHeight > slide.clientHeight + tolerance) issues.push('slide overflow');
        if (document.documentElement.scrollWidth > innerWidth + tolerance) issues.push('horizontal page overflow');
        if (boxes.length && minimumPadding < 4) issues.push('insufficient visible cell padding');
        return {viewport: [innerWidth, innerHeight], slideSize: [sr.width, sr.height], boxes: boxes.length,
          textRuns: textRuns.length, minimumPadding: boxes.length ? minimumPadding : null,
          connectors: slide.querySelectorAll('svg path, svg line, .dg-arrow').length, issues};
      });
      if (n === 3) await page.locator('.slide').screenshot({path: 'output/playwright/contract-clause-' + width + '.png'});
      results.push({slide: n, ...qa});
    }
  }
  return {results, errors};
}
