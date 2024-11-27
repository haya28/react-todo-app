// export type Category = {
//   id: string;
//   name: string;
//   color: string;
// };

export type Todo = {
  id: string;
  name: string;
  isDone: boolean;
  priority: number;
  deadline: Date | null; // 注意
  completed: boolean;
  repeat?: "daily" | "weekly" | "monthly"; // 繰り返し設定を追加
};
