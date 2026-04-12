import type { ButtonHTMLAttributes } from "react";
import clsx from "clsx";
import styles from "./Button.module.css";
import Spinner from "../Spinner/Spinner";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?:
    | "default"
    | "secondary"
    | "outline"
    | "destructive"
    | "ghost"
    | "link";
  size?: "default" | "xs" | "sm" | "lg" | "icon";
  loading?: boolean;
};

const SIZE_CLASSES: Record<string, string> = {
  default: styles.sizeDefault,
  xs: styles.sizeXs,
  sm: styles.sizeSm,
  lg: styles.sizeLg,
  icon: styles.sizeIcon,
};

export default function Button({
  variant = "default",
  size = "default",
  loading = false,
  className,
  children,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={clsx(
        styles.btn,
        styles[variant],
        SIZE_CLASSES[size],
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <span className={styles.icon}>
          <Spinner size="sm" />
        </span>
      )}
      {children}
    </button>
  );
}
