import { useState } from "react";
import { Input, Button } from "@/ui";
import { CircleArrowRight, type LucideIcon } from "lucide-react";
import { FILTER_OPTIONS } from "@/features/research/pages/search/constants";
import type { ResearchFilter } from "@/features/research/pages/search/types";
import { FilterChip } from "@/features/research/components";
import styles from "./SearchBox.module.css";

type SearchBoxProps = {
  showFilters?: boolean;
  onSearch: (query: string, filters: ResearchFilter[]) => void;
};

export const SearchBox = ({ showFilters, onSearch }: SearchBoxProps) => {
  const [inputValue, setInputValue] = useState("");
  const [filters, setFilters] = useState<Set<ResearchFilter>>(new Set());

  const handleFilter = (id: ResearchFilter) => {
    setFilters((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  return (
    <div className={styles.container}>
      <div className={styles.search}>
        <Input
          variant="ghost"
          type="search"
          placeholder="Where are we going? Tell me everything"
          value={inputValue}
          onInput={(e) => setInputValue(e.currentTarget.value)}
        />
        <Button
          variant="ghost"
          onClick={() => onSearch(inputValue, Array.from(filters))}
        >
          <CircleArrowRight className={styles.icon} />
        </Button>
      </div>
      {showFilters && (
        <div className={styles.filters}>
          {(
            Object.entries(FILTER_OPTIONS) as [
              ResearchFilter,
              { label: string; icon: LucideIcon }
            ][]
          ).map(([id, { label, icon }]) => (
            <FilterChip
              id={id}
              label={label}
              icon={icon}
              onClick={() => handleFilter(id)}
              selected={filters.has(id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};
