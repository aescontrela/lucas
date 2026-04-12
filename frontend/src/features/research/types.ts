import { z } from "zod";

export const DeltaEventSchema = z.object({
  event: z.literal("delta"),
  agent: z.string(),
  text: z.string(),
});

export const DoneEventSchema = z.object({
  event: z.literal("done"),
  agent: z.string().optional(),
});

export const ErrorEventSchema = z.object({
  event: z.literal("error"),
  agent: z.string().optional(),
  error: z.string().optional(),
  detail: z.string().optional(),
});

export const SSEEventSchema = z.discriminatedUnion("event", [
  DeltaEventSchema,
  DoneEventSchema,
  ErrorEventSchema,
]);

export type SSEEvent = z.infer<typeof SSEEventSchema>;
