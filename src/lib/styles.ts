// Style presets for FrameForge
export const STYLES = {
  viral: {
    bg: "#0A0A0A",
    accent: "#EF4444",
    accent2: "#F97316",
    text: "#FFFFFF",
    muted: "#94A3B8",
    gradient: "linear-gradient(135deg, #EF4444 0%, #F97316 100%)",
    font: "Inter, system-ui, sans-serif",
  },
  corporate: {
    bg: "#0F172A",
    accent: "#3B82F6",
    accent2: "#06B6D4",
    text: "#FFFFFF",
    muted: "#94A3B8",
    gradient: "linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%)",
    font: "Inter, system-ui, sans-serif",
  },
  product: {
    bg: "#050508",
    accent: "#7C3AED",
    accent2: "#06B6D4",
    text: "#FFFFFF",
    muted: "#94A3B8",
    gradient: "linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%)",
    font: "Inter, system-ui, sans-serif",
  },
  explainer: {
    bg: "#FAFAFA",
    accent: "#059669",
    accent2: "#0D9488",
    text: "#0F172A",
    muted: "#64748B",
    gradient: "linear-gradient(135deg, #059669 0%, #0D9488 100%)",
    font: "Inter, system-ui, sans-serif",
  },
} as const;

export type StyleName = keyof typeof STYLES;

// Voice presets mapping to edge-tts
export const VOICE_PRESETS = {
  af_heart: { name: "Aria (Warm)", edgeVoice: "en-US-AriaNeural", gender: "female" },
  af_nicole: { name: "Jenny (Professional)", edgeVoice: "en-US-JennyNeural", gender: "female" },
  am_adam: { name: "Guy (Casual)", edgeVoice: "en-US-GuyNeural", gender: "male" },
  am_michael: { name: "Christopher (Deep)", edgeVoice: "en-US-ChristopherNeural", gender: "male" },
  bf_emma: { name: "Sonia (British)", edgeVoice: "en-GB-SoniaNeural", gender: "female" },
  bm_george: { name: "Thomas (Formal)", edgeVoice: "en-GB-ThomasNeural", gender: "male" },
} as const;

export type VoicePreset = keyof typeof VOICE_PRESETS;

// Scene types
export interface TitleSceneData {
  type: "title";
  title: string;
  subtitle: string;
  duration: number; // frames at 30fps
}

export interface BulletListSceneData {
  type: "bullets";
  title: string;
  items: string[];
  duration: number;
}

export interface ComparisonSceneData {
  type: "comparison";
  title: string;
  left: { label: string; items: string[] };
  right: { label: string; items: string[] };
  duration: number;
}

export interface CounterSceneData {
  type: "counter";
  title: string;
  values: { label: string; end: number; prefix?: string; suffix?: string }[];
  duration: number;
}

export interface CTASceneData {
  type: "cta";
  title: string;
  subtitle: string;
  duration: number;
}

export type SceneData = TitleSceneData | BulletListSceneData | ComparisonSceneData | CounterSceneData | CTASceneData;

export interface VideoConfig {
  topic: string;
  style: StyleName;
  scenes: SceneData[];
  voicePreset: VoicePreset;
  format: "16:9" | "9:16" | "1:1";
}