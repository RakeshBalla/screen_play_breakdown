export const classifyElements = (elements) => {
  return elements.map((element) => ({
    ...element,
    id: `${element.sceneNumber}-${element.lineNumber}`,
  }));
};