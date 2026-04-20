import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, Audio } from "remotion";
import { TitleScene } from "./TitleScene";
import { BulletListScene } from "./BulletListScene";
import { ComparisonScene } from "./ComparisonScene";
import { CounterScene } from "./CounterScene";
import { CTAScene } from "./CTAScene";
import type { SceneData, StyleName, VideoConfig } from "../lib/styles";

// Calculate cumulative start frames for each scene
function getSceneStarts(scenes: SceneData[]): number[] {
  let acc = 0;
  return scenes.map((s) => {
    const start = acc;
    acc += s.duration;
    return start;
  });
}

export const FullVideo: React.FC<VideoConfig> = ({ topic, style = "viral", scenes, voicePreset }) => {
  const starts = getSceneStarts(scenes);
  const totalDuration = scenes.reduce((sum, s) => sum + s.duration, 0);

  return (
    <AbsoluteFill>
      {scenes.map((scene, i) => {
        const from = starts[i];

        switch (scene.type) {
          case "title":
            return (
              <Sequence key={i} from={from} durationInFrames={scene.duration}>
                <TitleScene title={scene.title} subtitle={scene.subtitle} style={style} />
              </Sequence>
            );
          case "bullets":
            return (
              <Sequence key={i} from={from} durationInFrames={scene.duration}>
                <BulletListScene title={scene.title} items={scene.items} style={style} />
              </Sequence>
            );
          case "comparison":
            return (
              <Sequence key={i} from={from} durationInFrames={scene.duration}>
                <ComparisonScene title={scene.title} left={scene.left} right={scene.right} style={style} />
              </Sequence>
            );
          case "counter":
            return (
              <Sequence key={i} from={from} durationInFrames={scene.duration}>
                <CounterScene title={scene.title} values={scene.values} style={style} />
              </Sequence>
            );
          case "cta":
            return (
              <Sequence key={i} from={from} durationInFrames={scene.duration}>
                <CTAScene title={scene.title} subtitle={scene.subtitle} style={style} />
              </Sequence>
            );
          default:
            return null;
        }
      })}

      {/* Voiceover audio will be added here by the pipeline */}
      {/* <Audio src={staticFile("voiceover.mp3")} /> */}
    </AbsoluteFill>
  );
};