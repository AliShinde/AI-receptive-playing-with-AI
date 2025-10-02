import React from 'react';

function TaskList({ tasks }) {
  return (
    <ul className="space-y-2">
      {tasks.map((task, index) => (
        <li key={index} className="p-3 border rounded bg-white dark:bg-gray-800">
          <div className="font-semibold">{task.text}</div>
          <div className="text-sm text-gray-600 dark:text-gray-300">
            📅 {task.date} | 🗂️ {task.category}
          </div>
        </li>
      ))}
    </ul>
  );
}

export default TaskList;
