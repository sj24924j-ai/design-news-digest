import DateSelector from "./DateSelector";

interface Props {
  dates: string[];
  selectedDate: string;
  isLatest: boolean;
  updatedAt: string | null;
  onChangeDate: (date: string) => void;
}

function formatUpdatedAt(iso: string | null): string {
  if (!iso) return "";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleString("ja-JP", {
    month: "numeric",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function Header({ dates, selectedDate, isLatest, updatedAt, onChangeDate }: Props) {
  return (
    <header className="app-header">
      <div className="app-header__title">
        <h1>デザインニュース ダイジェスト</h1>
        <p className="app-header__subtitle">
          {isLatest && updatedAt
            ? `本日 更新: ${formatUpdatedAt(updatedAt)}`
            : "過去のダイジェストを表示中"}
        </p>
      </div>
      <DateSelector dates={dates} selectedDate={selectedDate} onChange={onChangeDate} />
    </header>
  );
}
