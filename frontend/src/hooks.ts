import { useCallback, useEffect, useState } from "react";
import { useSearchParams } from "react-router";

interface FetchState<T> {
  data?: T;
  error?: Error;
  loading: boolean;
}

export function useFetch<T>(fn: () => Promise<T>, deps: unknown[]) {
  const [state, setState] = useState<FetchState<T>>({ loading: true });
  const [tick, setTick] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setState((s) => ({ ...s, loading: true, error: undefined }));
    fn().then(
      (data) => !cancelled && setState({ data, loading: false }),
      (error: Error) => !cancelled && setState({ error, loading: false }),
    );
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, tick]);

  const reload = useCallback(() => setTick((t) => t + 1), []);
  return { ...state, reload };
}

export function useQueryState() {
  const [params, setParams] = useSearchParams();

  const get = (key: string) => params.get(key) ?? "";
  const set = (key: string, value: string) => {
    const next = new URLSearchParams(params);
    if (value) next.set(key, value);
    else next.delete(key);
    if (key !== "page") next.delete("page");
    setParams(next);
  };
  const page = Number(params.get("page") ?? 1) || 1;

  return { get, set, page, setPage: (p: number) => set("page", p > 1 ? String(p) : "") };
}
