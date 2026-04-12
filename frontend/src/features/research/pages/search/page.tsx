import { Text } from "../../../../ui";
import { SearchBox } from "../../components";
import { useResearch } from "../../hooks";
import { FILTER_OPTIONS } from "./constants";
import styles from "./page.module.css";
import { useNavigate, useOutletContext } from "react-router";

export const Search = () => {
  const navigate = useNavigate();
  const { search } = useOutletContext<ReturnType<typeof useResearch>>();

  return (
    <div className={styles.container}>
      <Text as="h1" font="heading" size="xl" weight="bold">
        Where to?
      </Text>
      <SearchBox
        showFilters
        onSearch={(query, filters) => {
          const prefs = filters.map((f) => FILTER_OPTIONS[f].label).join(", ");
          search(prefs ? `Travel preferences: ${prefs} for ${query}` : query);
          navigate(`/thread?q=${encodeURIComponent(query)}`);
        }}
      />
    </div>
  );
};
