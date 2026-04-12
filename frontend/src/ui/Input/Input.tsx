import styles from "./Input.module.css";

type InputProps = React.ComponentProps<"input"> & {
  variant?: "default" | "ghost";
};

export default function Input({
  variant = "default",
  className,
  ...inputProps
}: InputProps) {
  return (
    <input
      className={`${styles.base} ${styles[variant]} ${className ?? ""}`}
      {...inputProps}
    />
  );
}
