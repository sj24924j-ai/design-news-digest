interface Props {
  dates: string[];
  selectedDate: string;
  onChange: (date: string) => void;
}

function formatDateLabel(date: string, isLatest: boolean): string {
  const [, month, day] = date.split("-");
  const label = `${Number(month)}/${Number(day)}`;
  return isLatest ? `${label}（最新）` : label;
}

export default function DateSelector({ dates, selectedDate, onChange }: Props) {
  return (
    <label className="date-selector">
      <span className="date-selector__label">日付</span>
      <select value={selectedDate} onChange={(e) => onChange(e.target.value)}>
        {dates.map((date, index) => (
          <option key={date} value={date}>
            {formatDateLabel(date, index === 0)}
          </option>
        ))}
      </select>
    </label>
  );
}
