import { useParams } from "react-router-dom";

export default function UserPage() {
  const { id } = useParams<{ id: string }>();
  return (
    <div className="px-4 py-6 sm:px-0">
      <h1 className="text-2xl font-bold">User</h1>
      <p className="mt-2 text-neutral-500 dark:text-neutral-400">
        Profile and preferences for <code className="font-mono">{id}</code>.
      </p>
    </div>
  );
}
