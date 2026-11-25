export const dash = "—";

export function fmtDate(value: string | null | undefined): string {
  return value ? new Date(value).toLocaleString("uk-UA") : dash;
}

export function fmtSec(value: number | null | undefined): string {
  if (value === null || value === undefined) return dash;
  const h = Math.floor(value / 3600);
  const m = Math.floor((value % 3600) / 60);
  const s = value % 60;
  if (h) return `${h} год ${m} хв`;
  if (m) return `${m} хв ${s} с`;
  return `${s} с`;
}

export function fmtBool(value: boolean | null | undefined): string {
  if (value === null || value === undefined) return dash;
  return value ? "так" : "ні";
}

export function fmtScore(value: string | null | undefined): string {
  return value === null || value === undefined ? dash : Number(value).toFixed(1);
}

export function text(value: string | number | null | undefined): string {
  return value === null || value === undefined || value === "" ? dash : String(value);
}
