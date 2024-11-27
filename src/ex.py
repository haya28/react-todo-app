import { useState, useEffect } from "react";
import { Todo, Category } from "./types";
import { initTodos } from "./initTodos";
import { initCategories } from "./initCategories";
import dayjs from "dayjs";

const App = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  // カテゴリーの追加機能
  const addCategory = (name: string, color: string) => {
    const newCategory: Category = {
      id: uuid(),
      name,
      color
    };
    setCategories([...categories, newCategory]);
  };

  // 繰り返しタスクの処理
  const processRecurringTasks = () => {
    const now = new Date();
    const updatedTodos = todos.map(todo => {
      if (todo.isRecurring && todo.isDone) {
        let shouldReset = false;
        switch (todo.recurringInterval) {
          case 'daily':
            shouldReset = dayjs(now).diff(todo.lastCompletedAt, 'day') >= 1;
            break;
          case 'weekly':
            shouldReset = dayjs(now).diff(todo.lastCompletedAt, 'week') >= 1;
            break;
          case 'monthly':
            shouldReset = dayjs(now).diff(todo.lastCompletedAt, 'month') >= 1;
            break;
          case 'yearly':
            shouldReset = dayjs(now).diff(todo.lastCompletedAt, 'year') >= 1;
            break;
        }

        if (shouldReset) {
          return {
            ...todo,
            isDone: false,
            lastCompletedAt: undefined
          };
        }
      }
      return todo;
    });

    setTodos(updatedTodos);
  };

  // 拡張されたタスク追加機能
  const addNewTodo = () => {
    const newTodo: Todo = {
      id: uuid(),
      name: newTodoName,
      isDone: false,
      priority: newTodoPriority,
      deadline: newTodoDeadline,
      categoryId: selectedCategory || undefined,
      isRecurring: isRecurring, // 新しいステート
      recurringInterval: recurringInterval, // 新しいステート
    };
    setTodos([...todos, newTodo]);
    // リセット処理
  };

  // タスク完了時の拡張
  const updateIsDone = (id: string, value: boolean) => {
    const updatedTodos = todos.map(todo => {
      if (todo.id === id) {
        return {
          ...todo,
          isDone: value,
          lastCompletedAt: value ? new Date() : undefined
        };
      }
      return todo;
    });
    setTodos(updatedTodos);
  };

  return (
    <div>
      {/* カテゴリー選択 */}
      <div className="flex gap-2">
        {categories.map(category => (
          <button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`
              ${category.color} 
              ${selectedCategory === category.id ? 'ring-2 ring-blue-500' : ''}
              px-2 py-1 rounded
            `}
          >
            {category.name}
          </button>
        ))}
      </div>

      {/* 繰り返しタスクのオプション */}
      <div>
        <label>
          <input
            type="checkbox"
            checked={isRecurring}
            onChange={() => setIsRecurring(!isRecurring)}
          />
          繰り返しタスク
        </label>
        {isRecurring && (
          <select 
            value={recurringInterval}
            onChange={(e) => setRecurringInterval(e.target.value as RecurringInterval)}
          >
            <option value="daily">毎日</option>
            <option value="weekly">毎週</option>
            <option value="monthly">毎月</option>
            <option value="yearly">毎年</option>
          </select>
        )}
      </div>
    </div>
  );
};

// TodoItem.tsx (追加の表示)
const TodoItem = ({ todo, category }) => {
  return (
    <div>
      {/* カテゴリー表示 */}
      {category && (
        <div 
          className={`
            inline-block px-2 py-1 rounded text-xs 
            ${category.color}
          `}
        >
          {category.name}
        </div>
      )}

      {/* 繰り返しタスク表示 */}
      {todo.isRecurring && (
        <div className="text-sm text-gray-500">
          {todo.recurringInterval}間隔で繰り返し
        </div>
      )}
    </div>
  );
};