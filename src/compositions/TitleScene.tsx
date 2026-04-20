import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { STYLES, type StyleName } from "../lib/styles";

export const TitleScene: React.FC<{
  title: string;
  subtitle: string;
  style?: StyleName;
  duration?: number;
}> = ({ title, subtitle, style = "viral" }) => {
  const frame = useCurrentFrame();
  const s = STYLES[style];

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
  const titleY = interpolate(frame, [0, 20], [40, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const subOpacity = interpolate(frame, [15, 35], [0, 1], { extrapolateRight: "clamp" });
  const subY = interpolate(frame, [15, 35], [20, 0], { extrapolateRight: "clamp" });
  const orbScale = interpolate(frame, [0, 150], [0.8, 1.2]);

  return (
    <AbsoluteFill style={{ background: s.bg, fontFamily: s.font, color: s.text, overflow: "hidden" }}>
      {/* Background orbs */}
      <div style={{ position: "absolute", width: 600, height: 600, borderRadius: "50%", background: `radial-gradient(circle, ${s.accent}33, transparent 70%)`, filter: "blur(80px)", top: -100, left: -100, transform: `scale(${orbScale})` }} />
      <div style={{ position: "absolute", width: 400, height: 400, borderRadius: "50%", background: `radial-gradient(circle, ${s.accent2}22, transparent 70%)`, filter: "blur(60px)", bottom: -50, right: -50, transform: `scale(${orbScale * 0.9})` }} />

      {/* Content */}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div style={{ opacity: titleOpacity, transform: `translateY(${titleY}px)`, textAlign: "center" }}>
          <h1 style={{ fontSize: 80, fontWeight: 900, lineHeight: 1.05, margin: 0, background: s.gradient, WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
            {title}
          </h1>
        </div>
        <div style={{ opacity: subOpacity, transform: `translateY(${subY}px)`, marginTop: 24 }}>
          <p style={{ fontSize: 28, color: s.muted, fontWeight: 500, margin: 0 }}>{subtitle}</p>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};