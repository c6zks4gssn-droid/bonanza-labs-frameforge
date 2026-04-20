import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { STYLES, type StyleName } from "../lib/styles";

export const CounterScene: React.FC<{
  title: string;
  values: { label: string; end: number; prefix?: string; suffix?: string }[];
  style?: StyleName;
}> = ({ title, values, style = "viral" }) => {
  const frame = useCurrentFrame();
  const s = STYLES[style];

  const titleOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: s.bg, fontFamily: s.font, color: s.text, padding: 100 }}>
      <div style={{ opacity: titleOpacity, marginBottom: 80, textAlign: "center" }}>
        <h2 style={{ fontSize: 48, fontWeight: 800, margin: 0, background: s.gradient, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>{title}</h2>
      </div>

      <div style={{ display: "flex", justifyContent: "center", gap: 80 }}>
        {values.map((v, i) => {
          const cardOpacity = interpolate(frame, [15 + i * 15, 30 + i * 15], [0, 1], { extrapolateRight: "clamp" });
          const cardY = interpolate(frame, [15 + i * 15, 30 + i * 15], [30, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
          // Animate number from 0 to end over 60 frames starting at frame 20+i*15
          const progress = interpolate(frame, [20 + i * 15, 80 + i * 15], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
          const current = Math.round(progress * v.end);

          return (
            <div key={i} style={{ opacity: cardOpacity, transform: `translateY(${cardY}px)`, textAlign: "center", padding: "40px 50px", borderRadius: 24, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
              <div style={{ fontSize: 72, fontWeight: 900, background: s.gradient, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", lineHeight: 1 }}>
                {v.prefix || ""}{current}{v.suffix || ""}
              </div>
              <div style={{ fontSize: 20, color: s.muted, fontWeight: 600, marginTop: 12 }}>{v.label}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};