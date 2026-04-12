import {
  Binoculars,
  Footprints,
  HouseHeart,
  MountainSnow,
  Music,
  Telescope,
} from "lucide-react";

export const FILTER_OPTIONS = {
  local_life: { label: "Local Life", icon: Binoculars },
  festivals_events: { label: "Festivals & Events", icon: Music },
  wildlife_nature: { label: "Wildlife & Nature", icon: MountainSnow },
  slow_travel: { label: "Slow Travel", icon: Footprints },
  hidden_gems: { label: "Hidden Gems", icon: Telescope },
  family_kids: { label: "Family & Kids", icon: HouseHeart },
} as const;
