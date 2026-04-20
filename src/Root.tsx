import { Composition } from "remotion";
import { TitleScene } from "./compositions/TitleScene";
import { BulletListScene } from "./compositions/BulletListScene";
import { ComparisonScene } from "./compositions/ComparisonScene";
import { CounterScene } from "./compositions/CounterScene";
import { CTAScene } from "./compositions/CTAScene";
import { FullVideo } from "./compositions/FullVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="FullVideo"
        component={FullVideo}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          topic: "Bonanza Labs",
          style: "viral" as const,
          scenes: [
            { type: "title", title: "Bonanza Labs", subtitle: "Open Source AI Tools", duration: 60 },
            { type: "bullets", title: "What We Build", items: ["FrameForge — AI Video", "Fork Doctor — Repo Health", "Agent Wallet — AI Payments"], duration: 60 },
            { type: "comparison", title: "Why Us?", left: { label: "Others", items: ["Closed source", "No voice cloning", "$190/mo"] }, right: { label: "Bonanza Labs", items: ["Open source", "Voice cloning", "Free"] }, duration: 60 },
            { type: "counter", title: "The Numbers", values: [{ label: "Projects", end: 5 }, { label: "Tests Passing", end: 10 }, { label: "Formats", end: 3 }], duration: 60 },
            { type: "cta", title: "Get Started", subtitle: "github.com/c6zks4gssn-droid", duration: 60 },
          ],
          voicePreset: "af_nicole",
        }}
      />
      <Composition id="TitleScene" component={TitleScene} durationInFrames={150} fps={30} width={1920} height={1080}
        defaultProps={{ title: "Hello World", subtitle: "FrameForge", style: "viral" as const }} />
      <Composition id="BulletListScene" component={BulletListScene} durationInFrames={150} fps={30} width={1920} height={1080}
        defaultProps={{ title: "Features", items: ["Fast", "Free", "Open Source"], style: "viral" as const }} />
      <Composition id="ComparisonScene" component={ComparisonScene} durationInFrames={150} fps={30} width={1920} height={1080}
        defaultProps={{ title: "Compare", left: { label: "A", items: ["1"] }, right: { label: "B", items: ["2"] }, style: "viral" as const }} />
      <Composition id="CounterScene" component={CounterScene} durationInFrames={150} fps={30} width={1920} height={1080}
        defaultProps={{ title: "Numbers", values: [{ label: "Count", end: 100 }], style: "viral" as const }} />
      <Composition id="CTAScene" component={CTAScene} durationInFrames={150} fps={30} width={1920} height={1080}
        defaultProps={{ title: "Get Started", subtitle: "Now", style: "viral" as const }} />
    </>
  );
};