interface SpinnerProps {
  label?: string;
  className?: string;
}

export default function Spinner({ label = "Loading", className = "" }: SpinnerProps) {
  return (
    <span role="status" aria-label={label} className={`inline-block ${className}`}>
      <span className="block h-5 w-5 animate-spin rounded-full border-2 border-neutral-300 border-t-neutral-900 dark:border-neutral-700 dark:border-t-neutral-100" />
    </span>
  );
}
