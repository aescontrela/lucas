import clsx from "clsx";
import styles from "./Spinner.module.css";

type SpinnerProps = {
  size?: "sm" | "default" | "lg";
  className?: string;
};

export default function Spinner({ size = "default", className }: SpinnerProps) {
  return <span className={clsx(styles.spinner, styles[size], className)} />;
}
