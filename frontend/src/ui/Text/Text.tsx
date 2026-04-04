import type { HTMLAttributes } from "react";
import clsx from "clsx";
import styles from "./Text.module.css";

type TextProps = HTMLAttributes<HTMLElement> & {
  as?: "p" | "span" | "h1" | "h2" | "h3" | "h4" | "label";
  size?: "xs" | "sm" | "base" | "lg" | "xl";
  weight?: "normal" | "medium" | "semibold" | "bold";
  muted?: boolean;
  font?: "heading" | "default";
};

export default function Text({
  as: Tag = "p",
  size = "base",
  font = "default",
  weight = "normal",
  muted = false,
  className,
  ...props
}: TextProps) {
  return (
    <Tag
      className={clsx(
        styles[size],
        styles[weight],
        muted && styles.muted,
        styles[font],
        className
      )}
      {...props}
    />
  );
}
