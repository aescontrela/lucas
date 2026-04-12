import { type LucideIcon } from "lucide-react";
import type { ResearchFilter } from "@/features/research/pages/search/types";
import { Text } from "@/ui";
import styles from "./FilterChip.module.css";

type FilterChipProps = {
  id: ResearchFilter;
  label: string;
  icon: LucideIcon;
  selected: boolean;
  onClick: (id: ResearchFilter) => void;
};

export const FilterChip = ({
  id,
  label,
  icon: Icon,
  selected,
  onClick,
}: FilterChipProps) => {
  return (
    <button
      key={id}
      type="button"
      onClick={() => onClick(id)}
      className={`${styles.pill} ${
        selected ? styles.filterOn : styles.filterOff
      }`}
    >
      <Icon size={12} />
      <Text size="sm" weight="medium">
        {label}
      </Text>
    </button>
  );
};
