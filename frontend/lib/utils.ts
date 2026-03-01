export function formatDistanceToNow(date: Date): string {
    const now = new Date();
    const diff = date.getTime() - now.getTime();

    if (diff < 0) return "overdue";

    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `in ${days}d ${hours % 24}h`;
    if (hours > 0) return `in ${hours}h ${minutes % 60}m`;
    return `in ${minutes}m`;
}

export function cn(...classes: (string | undefined | false | null)[]): string {
    return classes.filter(Boolean).join(" ");
}
