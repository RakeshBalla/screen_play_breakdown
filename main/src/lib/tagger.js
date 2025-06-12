export const tagElements = (elements) => {
  const keywordRules = {
    PROPS: /\b(gun|sword|phone|car|chair|table)\b/i,
    SOUND_FX: /\b(explosion|bang|crash|scream)\b/i,
    STUNTS: /\b(jump|fall|fight|chase)\b/i,
    LOCATION: /\b(kitchen|bedroom|street|park)\b/i,
  };

  return elements.map((element) => {
    const tags = [];

    if (element.type === 'scene_heading') {
      tags.push('LOCATION');
    } else if (element.type === 'character') {
      tags.push('CAST');
    } else if (element.type === 'shot') {
      tags.push('CAMERA');
    } else if (element.type === 'superimpose') {
      tags.push('SCREEN_TITLES');
    } else if (element.type === 'action') {
      for (const [category, regex] of Object.entries(keywordRules)) {
        if (regex.test(element.text)) {
          tags.push(category);
        }
      }
    }

    return { ...element, tags };
  });
};