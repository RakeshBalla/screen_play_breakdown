export const parseScript = (text) => {
  const lines = text.split('\n').map((line, index) => ({ line, lineNumber: index + 1 }));
  const elements = [];
  let currentScene = 0;
  let currentPage = 1;

  const sceneHeadingRegex = /^(INT\.|EXT\.|INT\.\/EXT\.|I\/E\.)\s+(.+?)\s+-\s+(.+)$/i;
  const characterRegex = /^[A-Z][A-Z\s]*(?:\s*\((V\.O\.|O\.C\.|O\.S\.)\))?$/;
  const parentheticalRegex = /^\(.+\)$/;
  const transitionRegex = /^(CUT TO|FADE OUT|DISSOLVE TO):$/i;
  const shotRegex = /^(CLOSE ON|ANGLE ON):/i;
  const superimposeRegex = /^SUPERIMPOSE:/i;

  let currentElement = null;

  for (const { line, lineNumber } of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    if (sceneHeadingRegex.test(trimmed)) {
      const [, prefix, location, time] = trimmed.match(sceneHeadingRegex);
      currentScene++;
      elements.push({
        type: 'scene_heading',
        text: trimmed,
        location,
        time,
        sceneNumber: currentScene,
        pageNumber: currentPage,
        lineNumber,
      });
      currentElement = null;
    } else if (characterRegex.test(trimmed)) {
      currentElement = {
        type: 'character',
        text: trimmed,
        sceneNumber: currentScene,
        pageNumber: currentPage,
        lineNumber,
      };
      elements.push(currentElement);
    } else if (parentheticalRegex.test(trimmed)) {
      elements.push({
        type: 'parenthetical',
        text: trimmed,
        sceneNumber: currentScene,
        pageNumber: currentPage,
        lineNumber,
      });
    } else if (transitionRegex.test(trimmed)) {
      elements.push({
        type: 'transition',
        text: trimmed,
        sceneNumber: currentScene,
        pageNumber: currentPage,
        lineNumber,
      });
    } else if (shotRegex.test(trimmed)) {
      elements.push({
        type: 'shot',
        text: trimmed,
        sceneNumber: currentScene,
        pageNumber: currentPage,
        lineNumber,
      });
    } else if (superimposeRegex.test(trimmed)) {
      elements.push({
        type: 'superimpose',
        text: trimmed,
        sceneNumber: currentScene,
        pageNumber: currentPage,
        lineNumber,
      });
    } else if (currentElement && currentElement.type === 'character') {
      elements.push({
        type: 'dialogue',
        text: trimmed,
        character: currentElement.text,
        sceneNumber: currentScene,
        pageNumber: currentPage,
        lineNumber,
      });
    } else {
      elements.push({
        type: 'action',
        text: trimmed,
        sceneNumber: currentScene,
        pageNumber: currentPage,
        lineNumber,
      });
    }

    // Simple page estimation: ~55 lines per page
    if (lineNumber % 55 === 0) currentPage++;
  }

  return elements;
};