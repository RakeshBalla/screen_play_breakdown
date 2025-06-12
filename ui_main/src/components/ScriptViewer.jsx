import React from 'react';

const ScriptViewer = ({ scriptElements, tags }) => {
  const getElementStyle = (element) => {
    const baseStyle = 'p-1';
    if (element.type === 'scene_heading') return `${baseStyle} font-bold uppercase`;
    if (element.type === 'character') return `${baseStyle} text-center`;
    if (element.type === 'dialogue') return `${baseStyle} mx-16`;
    if (element.type === 'parenthetical') return `${baseStyle} mx-12 italic`;
    if (element.type === 'transition') return `${baseStyle} text-right`;
    if (element.type === 'shot') return `${baseStyle} font-semibold`;
    if (element.type === 'superimpose') return `${baseStyle} font-semibold`;
    return baseStyle;
  };

  const getTagColor = (tag) => {
    return tags[tag]?.color || '#D1D5DB';
  };

  return (
    <div className="font-mono text-sm">
      {scriptElements.map((element) => (
        <div
          key={element.id}
          className={getElementStyle(element)}
          style={{
            backgroundColor: element.tags?.length && tags[element.tags[0]]?.visible ? getTagColor(element.tags[0]) + '20' : 'transparent',
          }}
        >
          <span className="mr-2">{element.sceneNumber}</span>
          {element.text}
          {element.tags?.length > 0 && (
            <span className="ml-2">
              {element.tags.map((tag) => (
                <span
                  key={tag}
                  className="inline-block h-2 w-2 rounded-full mr-1"
                  style={{ backgroundColor: getTagColor(tag) }}
                ></span>
              ))}
            </span>
          )}
        </div>
      ))}
    </div>
  );
};

export default ScriptViewer;