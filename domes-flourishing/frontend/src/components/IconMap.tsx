import {
  HeartPulse, Landmark, Palette, BookOpen, Sparkles, Users,
  Leaf, Building, Heart, Compass, Sun, Trophy,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

export const ICON_MAP: Record<string, LucideIcon> = {
  'heart-pulse': HeartPulse,
  landmark: Landmark,
  palette: Palette,
  'book-open': BookOpen,
  sparkles: Sparkles,
  users: Users,
  leaf: Leaf,
  building: Building,
  heart: Heart,
  compass: Compass,
  sun: Sun,
  trophy: Trophy,
};

export function DomainIcon({ icon, className, color }: { icon: string; className?: string; color?: string }) {
  const Icon = ICON_MAP[icon] || Compass;
  return <Icon className={className} style={color ? { color } : undefined} strokeWidth={1.6} />;
}
