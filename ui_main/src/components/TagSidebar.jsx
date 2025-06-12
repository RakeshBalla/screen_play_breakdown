import React, { useState } from 'react';

const TagSidebar = ({ tags, updateTags }) => {
  const [newTag, setNewTag] = useState('');
  const [newColor, setNewColor] = useState('#000000');

  const toggleTagVisibility = (tag) => {
    updateTags({
      ...tags,
      [tag]: { ...tags[tag], visible: !tags[tag].visible },
    });
  };

  const addTag = () => {
    if (newTag && !tags[newTag]) {
      updateTags({
        ...tags,
        [newTag]: { color: newColor, visible: true },
      });
      setNewTag('');
      setNewColor('#000000');
    }
  };

  const deleteTag = (tag) => {
    const newTags = { ...tags };
    delete newTags[tag];
    updateTags(newTags);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold">Tags</h2>
      {Object.entries(tags).map(([tag, { color, visible }]) => (
        <div key={tag} className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={visible}
              onChange={() => toggleTagVisibility(tag)}
              className="mr-2"
            />
            <span className="h-4 w-4 rounded-full mr-2" style={{ backgroundColor: color }}></span>
            <span>{tag}</span>
          </div>
          <button
            onClick={() => deleteTag(tag)}
            className="text-red-500 hover:text-red-700"
          >
            Delete
          </button>
        </div>
      ))}
      <div className="flex flex-col space-y-2">
        <input
          type="text"
          value={newTag}
          onChange={(e) => setNewTag(e.target.value)}
          placeholder="New tag name"
          className="border p-1 rounded"
        />
        <input
          type="color"
          value={newColor}
          onChange={(e) => setNewColor(e.target.value)}
          className="w-10 h-10"
        />
        <button
          onClick={addTag}
          className="bg-blue-500 text-white p-1 rounded hover:bg-blue-600"
        >
          Add Tag
        </button>
      </div>
    </div>
  );
};

export default TagSidebar;