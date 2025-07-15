import { useState, useEffect, useCallback, useRef } from 'react';

interface UseInfiniteScrollOptions {
  threshold?: number;
  rootMargin?: string;
}

interface UseInfiniteScrollReturn {
  isFetching: boolean;
  setIsFetching: (fetching: boolean) => void;
  lastElementRef: (node: HTMLElement | null) => void;
}

/**
 * Custom hook for infinite scrolling using Intersection Observer
 * @param fetchMore - Function to call when more data needs to be loaded
 * @param hasMore - Boolean indicating if there's more data to load
 * @param options - Intersection Observer options
 * @returns Object with isFetching state and ref for the last element
 */
export function useInfiniteScroll(
  fetchMore: () => Promise<void> | void,
  hasMore: boolean,
  options: UseInfiniteScrollOptions = {}
): UseInfiniteScrollReturn {
  const [isFetching, setIsFetching] = useState(false);
  const observer = useRef<IntersectionObserver | null>(null);

  const lastElementRef = useCallback(
    (node: HTMLElement | null) => {
      if (isFetching) return;
      if (observer.current) observer.current.disconnect();
      
      observer.current = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting && hasMore && !isFetching) {
            setIsFetching(true);
            Promise.resolve(fetchMore()).finally(() => {
              setIsFetching(false);
            });
          }
        },
        {
          threshold: options.threshold || 0.1,
          rootMargin: options.rootMargin || '100px',
        }
      );
      
      if (node) observer.current.observe(node);
    },
    [fetchMore, hasMore, isFetching, options.threshold, options.rootMargin]
  );

  useEffect(() => {
    return () => {
      if (observer.current) {
        observer.current.disconnect();
      }
    };
  }, []);

  return { isFetching, setIsFetching, lastElementRef };
}
