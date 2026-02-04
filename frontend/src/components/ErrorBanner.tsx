interface ErrorBannerProps {
  message: string;
  onClose: () => void;
}

export function ErrorBanner({ message, onClose }: ErrorBannerProps) {
  if (!message) return null;

  return (
    <div className="mb-6 flex items-center justify-between rounded-lg bg-red-50 p-4 text-red-800 border border-red-200 dark:bg-red-900/20 dark:text-red-200 dark:border-red-800 shadow-sm animate-fade-in">
      <div className="flex items-center gap-3">
        <span className="text-xl" role="img" aria-label="Error">
          ⚠️
        </span>
        <p className="text-sm font-medium">{message}</p>
      </div>
      <button
        onClick={onClose}
        className="rounded-md p-1.5 hover:bg-red-100 dark:hover:bg-red-800/40 transition-colors"
        aria-label="Fechar mensagem de erro"
      >
        ✕
      </button>
    </div>
  );
}
