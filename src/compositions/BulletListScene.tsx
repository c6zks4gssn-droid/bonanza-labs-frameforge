import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { STYLES, type StyleName } from "../lib/styles";

export const BulletListScene: React.FC<{
  title: string;
  items: string[];
  style?: StyleName;
}> = ({ title, items, style = "viral" }) => {
  const frame = useCurrentFrame();
  const s = STYLES[style];

  const titleOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: s.bg, fontFamily: s.font, color: s.text, padding: 120 }}>
      {/* Title */}
      <div style={{ opacity: titleOpacity, marginBottom: 60 }}>
        <h2 style={{ fontSize: 48, fontWeight: 800, margin: 0, background: s.gradient, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>{title}</h2>
      </div>

      {/* Items with stagger */}
      <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
        {items.map((item, i) => {
          const itemOpacity = interpolate(frame, [20 + i * 12, 35 + i * 12], [0, 1], { extrapolateRight: "clamp" });
          const itemX = interpolate(frame, [20 + i * 12, 35 + i * 12], [-30, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
          const dotScale = interpolate(frame, [25 + i * 12, 32 + i * 12], [0, 1], { extrapolateRight: "clamp" });

          return (
            <div key={i} style={{ opacity: itemOpacity, transform: `translateX(${itemX}px)`, display: "flex", alignItems: "center", gap: 20 }}>
              <div style={{ width: 16, height: 16, borderRadius: "50%", background: s.accent, transform: `scale(${dotScale})`, flexShrink: 0 }} />
              <span style={{ fontSize: 32, fontWeight: 600, color: s.text }}>{item}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};