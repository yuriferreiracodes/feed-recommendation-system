import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

/**
 * Catches render-time errors anywhere below it. Must stay a class component:
 * React exposes no hook equivalent of componentDidCatch.
 */
export default class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error("Unhandled render error:", error, info.componentStack);
  }

  private handleReset = () => {
    this.setState({ error: null });
  };

  render(): ReactNode {
    const { error } = this.state;
    if (!error) {
      return this.props.children;
    }
    return (
      <div className="flex min-h-full items-center justify-center bg-neutral-50 p-6 dark:bg-neutral-950">
        <div className="max-w-md text-center">
          <h1 className="text-xl font-semibold text-neutral-900 dark:text-neutral-100">
            Something went wrong
          </h1>
          <p className="mt-2 text-sm text-neutral-600 dark:text-neutral-400">{error.message}</p>
          <button
            type="button"
            onClick={this.handleReset}
            className="mt-6 rounded-md bg-neutral-900 px-4 py-2 text-sm font-medium text-white hover:bg-neutral-700 dark:bg-neutral-100 dark:text-neutral-900 dark:hover:bg-neutral-300"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }
}
