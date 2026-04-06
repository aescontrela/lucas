import { z } from "zod";

export const AgentTypeSchema = z.enum([
  "activities",
  "food",
  "culture",
  "safety",
  "logistics",
]);
export const EventTypeSchema = z.enum(["idle", "delta", "error", "done"]);

export const ResearchEventSchema = z.object({
  source: z.union([AgentTypeSchema, z.literal("system")]),
  status: EventTypeSchema,
  content: z.string().optional(),
  error: z.string().optional(),
});

export type AgentType = z.infer<typeof AgentTypeSchema>;
export type EventType = z.infer<typeof EventTypeSchema>;
export type ResearchEvent = z.infer<typeof ResearchEventSchema>;
