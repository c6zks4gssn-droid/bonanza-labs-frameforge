import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { STYLES, type StyleName } from "../lib/styles";

export const ComparisonScene: React.FC<{
  title: string;
  left: { label: string; items: string[] };
  right: { label: string; items: string[] };
  style?: StyleName;
}> = ({ title, left, right, style = "viral" }) => {
  const frame = useCurrentFrame();
  const s = STYLES[style];

  const titleOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });
  const leftX = interpolate(frame, [15, 35], [-60, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const leftOpacity = interpolate(frame, [15, 30], [0, 1], { extrapolateRight: "clamp" });
  const rightX = interpolate(frame, [20, 40], [60, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const rightOpacity = interpolate(frame, [20, 35], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: s.bg, fontFamily: s.font, color: s.text, padding: 100 }}>
      <div style={{ opacity: titleOpacity, marginBottom: 60, textAlign: "center" }}>
        <h2 style={{ fontSize: 48, fontWeight: 800, margin: 0, background: s.gradient, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>{title}</h2>
      </div>

      <div style={{ display: "flex", gap: 60, justifyContent: "center" }}>
        {/* Left column */}
        <div style={{ opacity: leftOpacity, transform: `translateX(${leftX}px)`, flex: 1, maxWidth: 500, padding: 40, borderRadius: 24, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
          <h3 style={{ fontSize: 28, fontWeight: 700, marginBottom: 24, color: s.muted }}>{left.label}</h3>
          {left.items.map((item, i) => {
            const io = interpolate(frame, [30 + i * 10, 40 + i * 10], [0, 1], { extrapolateRight: "clamp" });
            return <div key={i} style={{ opacity: io, fontSize: 22, marginBottom: 12, color: "#EF4444" }}>✗ {item}</div>;
          })}
        </div>

        {/* Right column */}
        <div style={{ opacity: rightOpacity, transform: `translateX(${rightX}px)`, flex: 1, maxWidth: 500, padding: 40, borderRadius: 24, background: `${s.accent}11`, border: `1px solid ${s.accent}33` }}>
          <h3 style={{ fontSize: 28, fontWeight: 700, marginBottom: 24, color: s.accent }}>{right.label}</h3>
          {right.items.map((item, i) => {
            const io = interpolate(frame, [35 + i * 10, 45 + i * 10], [0, 1], { extrapolateRight: "clamp" });
            return <div key={i} style={{ opacity: io, fontSize: 22, marginBottom: 12, color: "#22C55E" }}>✓ {item}</div>;
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};