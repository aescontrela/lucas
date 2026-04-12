import { z } from "zod";

export const ResearchFilterSchema = z.enum([
  "slow_travel",
  "family_kids",
  "festivals_events",
  "local_life",
  "hidden_gems",
  "wildlife_nature",
]);

export type ResearchFilter = z.infer<typeof ResearchFilterSchema>;
