import React, { useState } from 'react';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';

function App() {
  const [tasks, setTasks] = useState([]);

  const addTask = (task) => {
    setTasks([...tasks, task]);
  };

  return (
    <div className="min-h-screen p-6">
      <h1 className="text-3xl font-bold mb-4">📝 Fancy To-Do List</h1>
      <TaskForm onAddTask={addTask} />
      <TaskList tasks={tasks} />
      <div className="mt-6 p-4 bg-blue-100 dark:bg-blue-800 rounded">
        💡 Stay productive! "The secret of getting ahead is getting started."
      </div>
    </div>
  );
}

export default App;
